#!/usr/bin/env python3
"""Audit Dockerfiles and docker-compose files for security and best-practice issues."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SEVERITY_ORDER = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}


def audit_dockerfile(path: str) -> list[dict]:
    """Audit a single Dockerfile and return findings."""
    findings = []
    try:
        content = Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return [{"severity": "CRITICAL", "rule": "READ_ERROR", "message": f"Cannot read file: {e}", "line": 0}]

    lines = content.splitlines()
    has_user = False
    has_healthcheck = False
    run_count = 0
    from_count = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        upper = stripped.upper()

        # Check FROM tag
        if upper.startswith("FROM "):
            from_count += 1
            parts = stripped.split()
            if len(parts) >= 2:
                image = parts[1]
                if image.lower() != "scratch":
                    if ":" not in image or image.endswith(":latest"):
                        findings.append({
                            "severity": "WARNING",
                            "rule": "NO_TAG_OR_LATEST",
                            "message": f"Image '{image}' uses no tag or :latest — pin a specific version for reproducibility",
                            "line": i,
                        })

        # Check USER directive
        if upper.startswith("USER "):
            has_user = True

        # Check HEALTHCHECK
        if upper.startswith("HEALTHCHECK "):
            has_healthcheck = True

        # ADD vs COPY
        if upper.startswith("ADD ") and not any(x in stripped for x in [".tar", ".gz", ".bz2", "http://", "https://"]):
            findings.append({
                "severity": "WARNING",
                "rule": "ADD_INSTEAD_OF_COPY",
                "message": "Use COPY instead of ADD unless extracting archives or fetching URLs",
                "line": i,
            })

        # RUN count
        if upper.startswith("RUN "):
            run_count += 1

        # Secrets in ENV/ARG
        if upper.startswith("ENV ") or upper.startswith("ARG "):
            secret_patterns = [
                r"(?i)(password|secret|token|api_key|apikey|private_key|aws_secret)",
            ]
            for pat in secret_patterns:
                if re.search(pat, stripped):
                    findings.append({
                        "severity": "CRITICAL",
                        "rule": "SECRETS_IN_ENV",
                        "message": f"Possible secret in {stripped.split()[0]} directive — use build secrets or runtime injection instead",
                        "line": i,
                    })

        # Privileged port exposure
        if upper.startswith("EXPOSE "):
            ports = re.findall(r"\d+", stripped)
            for p in ports:
                if int(p) < 1024 and int(p) not in (80, 443, 8080, 8443):
                    findings.append({
                        "severity": "INFO",
                        "rule": "PRIVILEGED_PORT",
                        "message": f"Exposing privileged port {p} — ensure this is intended",
                        "line": i,
                    })

        # Curl pipe to shell
        if upper.startswith("RUN ") and ("curl" in stripped or "wget" in stripped) and ("|" in stripped) and ("sh" in stripped or "bash" in stripped):
            findings.append({
                "severity": "CRITICAL",
                "rule": "CURL_PIPE_SHELL",
                "message": "Piping curl/wget to shell is a security risk — download, verify, then execute",
                "line": i,
            })

        # No version pinning in apt-get/apk
        if upper.startswith("RUN ") and ("apt-get install" in stripped or "apk add" in stripped):
            if "=" not in stripped.split("install")[-1] if "install" in stripped else stripped:
                findings.append({
                    "severity": "INFO",
                    "rule": "NO_VERSION_PIN",
                    "message": "Consider pinning package versions for reproducible builds",
                    "line": i,
                })

    # Post-scan checks
    if not has_user and from_count > 0:
        findings.append({
            "severity": "CRITICAL",
            "rule": "ROOT_USER",
            "message": "No USER directive — container will run as root",
            "line": 0,
        })

    if not has_healthcheck and from_count > 0:
        findings.append({
            "severity": "WARNING",
            "rule": "NO_HEALTHCHECK",
            "message": "No HEALTHCHECK defined — orchestrators cannot monitor container health",
            "line": 0,
        })

    if run_count > 10:
        findings.append({
            "severity": "INFO",
            "rule": "EXCESSIVE_LAYERS",
            "message": f"{run_count} RUN instructions — consider consolidating to reduce image layers",
            "line": 0,
        })

    # Check for .dockerignore
    dockerfile_dir = Path(path).parent
    if not (dockerfile_dir / ".dockerignore").exists():
        findings.append({
            "severity": "INFO",
            "rule": "NO_DOCKERIGNORE",
            "message": "No .dockerignore found — consider adding one to reduce build context size",
            "line": 0,
        })

    return findings


def audit_compose(path: str) -> list[dict]:
    """Audit a docker-compose file and return findings."""
    findings = []
    try:
        content = Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return [{"severity": "CRITICAL", "rule": "READ_ERROR", "message": f"Cannot read file: {e}", "line": 0}]

    # Simple YAML-like parsing without requiring pyyaml
    lines = content.splitlines()
    current_service = None
    in_services = False
    has_mem_limit = False
    has_restart = False
    service_line = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        # Track services block
        if stripped.startswith("services:"):
            in_services = True
            continue

        if in_services and indent == 2 and stripped.endswith(":") and not stripped.startswith("-") and not stripped.startswith("#"):
            # Emit checks for previous service
            if current_service:
                if not has_mem_limit:
                    findings.append({
                        "severity": "WARNING",
                        "rule": "NO_RESOURCE_LIMITS",
                        "message": f"Service '{current_service}' has no memory/CPU limits — can consume unbounded resources",
                        "line": service_line,
                    })
                if not has_restart:
                    findings.append({
                        "severity": "INFO",
                        "rule": "NO_RESTART_POLICY",
                        "message": f"Service '{current_service}' has no restart policy",
                        "line": service_line,
                    })

            current_service = stripped.rstrip(":")
            service_line = i
            has_mem_limit = False
            has_restart = False
            continue

        if in_services and indent == 0 and stripped and not stripped.startswith("#"):
            # Exited services block
            in_services = False

        if not in_services or not current_service:
            continue

        # Check for privileged
        if "privileged:" in stripped and "true" in stripped.lower():
            findings.append({
                "severity": "CRITICAL",
                "rule": "PRIVILEGED_CONTAINER",
                "message": f"Service '{current_service}' runs in privileged mode — full host access",
                "line": i,
            })

        # Check network_mode: host
        if "network_mode:" in stripped and "host" in stripped.lower():
            findings.append({
                "severity": "WARNING",
                "rule": "HOST_NETWORK",
                "message": f"Service '{current_service}' uses host network — no network isolation",
                "line": i,
            })

        # Check sensitive volume mounts
        sensitive_paths = ["/etc", "/var/run/docker.sock", "/root", "/proc", "/sys"]
        if "volumes:" not in stripped and "- " in stripped and ":" in stripped:
            for sp in sensitive_paths:
                if sp in stripped:
                    findings.append({
                        "severity": "CRITICAL",
                        "rule": "SENSITIVE_MOUNT",
                        "message": f"Service '{current_service}' mounts sensitive path '{sp}'",
                        "line": i,
                    })

        # Check plaintext secrets in environment
        if re.search(r"(?i)(password|secret|token|api_key|apikey)[\s]*[:=]", stripped):
            if "${" not in stripped and "vault" not in stripped.lower():
                findings.append({
                    "severity": "CRITICAL",
                    "rule": "PLAINTEXT_SECRET",
                    "message": f"Service '{current_service}' may have plaintext secret in environment",
                    "line": i,
                })

        # Track resource limits
        if any(k in stripped for k in ["mem_limit", "memory:", "cpus:", "cpu_shares", "deploy:"]):
            has_mem_limit = True

        # Track restart policy
        if "restart:" in stripped:
            has_restart = True

    # Final service check
    if current_service:
        if not has_mem_limit:
            findings.append({
                "severity": "WARNING",
                "rule": "NO_RESOURCE_LIMITS",
                "message": f"Service '{current_service}' has no memory/CPU limits — can consume unbounded resources",
                "line": service_line,
            })
        if not has_restart:
            findings.append({
                "severity": "INFO",
                "rule": "NO_RESTART_POLICY",
                "message": f"Service '{current_service}' has no restart policy",
                "line": service_line,
            })

    return findings


def detect_file_type(path: str) -> str:
    """Detect whether a file is a Dockerfile or compose file."""
    name = Path(path).name.lower()
    if "dockerfile" in name:
        return "dockerfile"
    if "compose" in name or "docker-compose" in name:
        return "compose"
    # Peek at content
    try:
        first_lines = Path(path).read_text(encoding="utf-8", errors="ignore")[:500].upper()
        if "FROM " in first_lines:
            return "dockerfile"
        if "SERVICES:" in first_lines:
            return "compose"
    except Exception:
        pass
    return "unknown"


def scan_directory(dirpath: str) -> dict[str, list[dict]]:
    """Scan a directory for Docker files and audit them."""
    results = {}
    docker_patterns = [
        "Dockerfile", "Dockerfile.*", "*.dockerfile",
        "docker-compose.yml", "docker-compose.yaml",
        "docker-compose.*.yml", "docker-compose.*.yaml",
        "compose.yml", "compose.yaml",
    ]
    for root, _, files in os.walk(dirpath):
        for f in files:
            fpath = os.path.join(root, f)
            ftype = detect_file_type(fpath)
            if ftype == "dockerfile":
                results[fpath] = audit_dockerfile(fpath)
            elif ftype == "compose":
                results[fpath] = audit_compose(fpath)
    return results


def format_text(results: dict[str, list[dict]]) -> str:
    """Format findings as human-readable text."""
    if not results:
        return "No Docker files found to audit."

    output = []
    total_critical = 0
    total_warning = 0
    total_info = 0

    for filepath, findings in results.items():
        sorted_findings = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f["severity"], 9))
        output.append(f"\n{'='*60}")
        output.append(f"File: {filepath}")
        output.append(f"{'='*60}")

        if not findings:
            output.append("  ✅ No issues found")
            continue

        for f in sorted_findings:
            icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}.get(f["severity"], "⚪")
            loc = f" (line {f['line']})" if f["line"] else ""
            output.append(f"  {icon} [{f['severity']}] {f['rule']}{loc}")
            output.append(f"     {f['message']}")
            if f["severity"] == "CRITICAL":
                total_critical += 1
            elif f["severity"] == "WARNING":
                total_warning += 1
            else:
                total_info += 1

    output.append(f"\n{'='*60}")
    output.append(f"Summary: {total_critical} critical, {total_warning} warnings, {total_info} info")
    if total_critical > 0:
        output.append("⚠️  Critical issues found — address before deploying")
    output.append(f"{'='*60}")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Audit Dockerfiles and docker-compose files for security and best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s Dockerfile
  %(prog)s docker-compose.yml
  %(prog)s ./project/
  %(prog)s Dockerfile --format json
""",
    )
    parser.add_argument("target", help="Dockerfile, docker-compose file, or directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Error: '{args.target}' not found", file=sys.stderr)
        sys.exit(1)

    if target.is_dir():
        results = scan_directory(str(target))
    else:
        ftype = detect_file_type(str(target))
        if ftype == "dockerfile":
            results = {str(target): audit_dockerfile(str(target))}
        elif ftype == "compose":
            results = {str(target): audit_compose(str(target))}
        else:
            print(f"Error: Cannot determine file type for '{args.target}'", file=sys.stderr)
            sys.exit(1)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(format_text(results))

    # Exit code: 1 if any critical findings
    for findings in results.values():
        if any(f["severity"] == "CRITICAL" for f in findings):
            sys.exit(1)


if __name__ == "__main__":
    main()
