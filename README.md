# DeepConsensus-utils

Some scripts for accelerating subreads-to-CCS alignment step of [DeepConsensus](https://github.com/google/deepconsensus) pipeline.

Before running DeepConsensus, subreads should be aligned to CCS correctly. In the [Quick start for DeepConsensus](https://github.com/google/deepconsensus/blob/main/docs/quick_start.md), 
this step is achieved by an 'all subreads to all CCS reads alignment' (pbmm2 align) and a following molecule-name-based filtering. However, the all-to-all alignment could be extremely slow.
A simple strategy is split the CCS reads and subreads into trunks based on molecule names before alignment. After trunk-to-trunk alignment, merge output BAM files using `samtools merge`.

## split_ccs_fasta.py

A script for splitting CCS reads by movie names.

### usage

```Bash
$ ./split_ccs_fasta.py -h

usage: split_ccs_fasta.py [-h] total_fasta movie_names [movie_names ...]

positional arguments:
  total_fasta  a fasta file of CCS reads from plural movies
  movie_names  the movies need to be split

optional arguments:
  -h, --help   show this help message and exit
```

If you have a single `ccs.fasta` containing CCS reads from three movies (`m111111_222222_333333`, `m444444_555555_666666`, `m777777_888888_999999`):

```Bash
./split_ccs_fasta.py ccs.fasta m111111_222222_333333 m444444_555555_666666 m777777_888888_999999
```

You will get three output fasta files: `m111111_222222_333333.ccs.fasta`, `m444444_555555_666666.ccs.fasta`, `m777777_888888_999999.ccs.fasta`


## split_subreads_ccs_trunks.py

A script for splitting CCS reads and subreads from a same movie into trunks.

### usage

```Bash
$ ./split_subreads_ccs_trunks.py -h

usage: split_subreads_ccs_trunks.py [-h] [--nchunks NCHUNKS] [--threads THREADS] ccs_fasta subread_bam prefix

positional arguments:
  ccs_fasta          a fasta file of CCS reads from a single movie
  subread_bam        a bam file of subreads from a corresponding single movie
  prefix             a prefix for output files (e.g. you can use the movie name)

optional arguments:
  -h, --help         show this help message and exit
  --nchunks NCHUNKS  number of chunks, default 200
  --threads THREADS  number of threads for running samtools, default 28
```

You can split CCS reads `m111111_222222_333333.ccs.fasta` and corresponding subreads `m111111_222222_333333.subreads.bam` into 100 chunks by:

```Bash
./split_subreads_ccs_trunks.py m111111_222222_333333.ccs.fasta m111111_222222_333333.subreads.bam m111111_222222_333333 --nchunks 100
```

