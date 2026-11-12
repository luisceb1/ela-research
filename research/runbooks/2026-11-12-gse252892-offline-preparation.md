# GSE252892 offline descriptor preparation

Use the exact reviewed commit supplied with PR #76. Preserve the old detached checkout and its environment. Fetch repository code only, then add a new detached worktree; if the new directory already exists, stop rather than deleting it. No FASTQ is fetched by this procedure. Substitute the reviewed commit for REVIEWED_COMMIT.

```powershell
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto fetch origin REVIEWED_COMMIT
wsl -d Ubuntu-24.04 -- git -C /home/luisceb/proyectos/ela-research-piloto worktree add --detach /home/luisceb/proyectos/ela-local-20261112 REVIEWED_COMMIT
wsl -d Ubuntu-24.04 -- /home/luisceb/proyectos/ela-research-piloto/.venv/bin/python /home/luisceb/proyectos/ela-local-20261112/scripts/prepare_gse252892_local.py --index-dir /home/luisceb/ela-piloto-real-01-index-recovery-01-extracted-01/index/files/hg38 --aligner /home/luisceb/ela-tools/hisat2-2.2.3/hisat2-align-s --inspector /home/luisceb/ela-tools/hisat2-2.2.3/hisat2-inspect-s --output /home/luisceb/ela-gse252892-prepared-20261112.json
```

Stop on any error. Success prints `prepared_disabled`, 9 verified index members, 4 file entries, advertised input bytes 12,826,593,031 and raw bytes downloaded 0, with the descriptor SHA256. Share that small terminal summary for review; do not edit the descriptor to activate anything. Rechecking the index reads about 4.4 GiB from local disk and can take minutes. No new packages are needed for this preparer. The user-reported existing environment is Python 3.12.3/PySAM 0.23.3.

The eventual runner, reference/assay review, measured local resources and explicit transfer/disk/time limits are unresolved. Preparing a descriptor is neither permission nor an implementation for downloading 12.83 GB. Small prefixes would test software/resources only. No KD/control inference, functional recovery or clinical claim follows.
