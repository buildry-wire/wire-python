# Releasing wire-python (PyPI: wirepayment)

Releases publish to PyPI over **OIDC Trusted Publishing** — no API token is stored.

## One-time PyPI setup (browser, maintainer)
1. Sign in at https://pypi.org.
2. Account → Publishing → "Add a new pending publisher":
   - PyPI Project Name: `wirepayment`
   - Owner: `buildry-wire`
   - Repository name: `wire-python`
   - Workflow name: `release.yml`
   - Environment: (leave blank)
3. Save. The first tagged release will create the project automatically.

## Cut a release
1. Bump `version` in `pyproject.toml`.
2. Move changelog items under `## [x.y.z] - YYYY-MM-DD`.
3. Commit on `main`, then:
   ```bash
   git tag vX.Y.Z   # must equal pyproject version
   git push origin vX.Y.Z
   ```
4. The `release` workflow builds, checks, and publishes via OIDC.

## Verify
```bash
pip install wirepayment==X.Y.Z
```
