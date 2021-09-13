#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Xiaofei Zeng
# Email: xiaofei_zeng@whu.edu.cn
# Created Time: 2021-09-11 15:02


import argparse
import math
import os


def parse_ccs(ccs):
    ccs_dict = dict()
    ccs_ID_list = list()
    with open(ccs) as f:
        for line in f:
            if line.startswith('>'):
                ID = line.split()[0][1:]
                ccs_ID_list.append(ID)
                ccs_dict[ID] = ''
            else:
                ccs_dict[ID] += line
    return ccs_dict, ccs_ID_list


def split_chunks(ccs_dict, ccs_ID_list, prefix, nchunks):
    ccs_num = len(ccs_ID_list)
    chunk_size = math.ceil(ccs_num / nchunks)
    chunk_ID_list = list()
    chunk_dict = dict()
    for n in range(nchunks):
        chunk_ID = 'ccs_chunk_{}'.format(n+1)
        chunk_ID_list.append(chunk_ID)
        with open('{}.{}.fasta'.format(prefix, chunk_ID), 'w') as f:
            for ID in ccs_ID_list[n*chunk_size: (n+1)*chunk_size]:
                chunk_dict[ID.rsplit('/', 1)[0]] = chunk_ID
                f.write('>{}\n'.format(ID))
                f.write(ccs_dict[ID])
    return chunk_ID_list, chunk_dict


def parse_subreads(bam, chunk_ID_list, chunk_dict, prefix, threads):
    header = os.popen('samtools view -H {}'.format(bam)).read()
    fp_dict = dict()
    for chunk_ID in chunk_ID_list:
        fp_dict[chunk_ID] = open('{}.{}.sam'.format(prefix, chunk_ID), 'w')
        fp_dict[chunk_ID].write(header)
    with os.popen('samtools view {} -@ {}'.format(bam, threads)) as f:
        for line in f:
            subread_ID = line.split()[0]
            if subread_ID.rsplit('/', 1)[0] in chunk_dict: 
                fp = fp_dict[chunk_dict[subread_ID.rsplit('/', 1)[0]]]
                fp.write(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ccs_fasta', help='a fasta file of CCS reads from a single movie')
    parser.add_argument('subread_bam', help='a bam file of subreads from a corresponding single movie')
    parser.add_argument('prefix', help='a prefix for output files (e.g. you can use the movie name)')
    parser.add_argument('--nchunks', type=int, default=200, help='number of chunks, default %(default)s')
    parser.add_argument('--threads', type=int, default=28, help='number of threads for running samtools, default %(default)s')
    args = parser.parse_args()

    ccs_dict, ccs_ID_list = parse_ccs(args.ccs_fasta)
    chunk_ID_list, chunk_dict = split_chunks(ccs_dict, ccs_ID_list, args.prefix, args.nchunks)
    parse_subreads(args.subread_bam, chunk_ID_list, chunk_dict, args.prefix, args.threads)

if __name__ == '__main__':
    main()
