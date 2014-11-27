import os
import shutil
import ftplib
from bcbio.provenance import do
from bcbio.distributed.transaction import tx_tmpdir, file_transaction
from bcbio.utils import chdir, safe_makedir


def _download_sra(fn_files, out_dir):
    """download sra files"""
    new_files = []
    cmd = ("wget --quiet {fn_sra} -O {tx_out_file}")
    for fn_sra in fn_files:
        fn_name = fn_sra.split('/')[-1]
        out_file = os.path.join(out_dir, fn_name)
        if not os.path.exists(out_file):
            with file_transaction(out_file) as tx_out_file:
                do.run(cmd.format(**locals()), "Download to %s" % (fn_sra))
        new_files.append(os.path.abspath(out_file))
    return new_files


def convert_fastq(files, paired=False):
    new_files = []
    paired = "" if paired else "--split-3"
    for sra_file in files:
        out_dir = os.path.dirname(sra_file)
        file_name = os.path.basename(sra_file).replace(".sra", "")
        fastq_file = os.path.join(out_dir, file_name)
        cmd = ("fastq-dump --split-3 -O {tmpdir} --gzip {sra_file}")
        if not os.path.exists(fastq_file):
            with tx_tmpdir(remove=False) as tmpdir:
                do.run(cmd.format(**locals()), "fastq-dump %s" % sra_file)
                shutil.move(os.path.join(tmpdir, file_name) + "*gz", out_dir)
        new_files.append(fastq_file) + ".fastq.gz" if not paired else new_files.append(make_paired(fastq_file))
    return new_files


def make_paired(prefix):
    return [prefix + "_1.fastq.gz", prefix + "_2.fastq.gz"]

def sra_check(files, out_dir, sample=None):
    """check if files are sra ftp"""
    print files
    issra = any([is_sra(fn[0]) for fn in files])
    if issra:
        out_dir = safe_makedir(os.path.join(out_dir, "tmp"))
        files = [_download_sra(fn, out_dir) for fn in files]
        files = [convert_fastq(fn) for fn in files]
    if sample:
        return (sample, files)
    return files


def is_sra(fn_file):
    return fn_file.find("ftp:") > -1 and fn_file.endswith("sra")
