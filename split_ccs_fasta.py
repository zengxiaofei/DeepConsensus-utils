#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Xiaofei Zeng
# Email: xiaofei_zeng@whu.edu.cn
# Created Time: 2021-09-09 23:30

import argparse


def split_fasta(total_fasta, movie_names):
    fp_dict = {movie: open('{}.ccs.fasta'.format(movie), 'w') for movie in movie_names}
    with open(total_fasta) as f:
        for line in f:
            if line.startswith('>'):
                movie = line.split()[0][1:].split('/')[0]
            fp_dict[movie].write(line)
    for movie, fp in fp_dict.items():
        fp.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('total_fasta', help='a fasta file of CCS reads from plural movies')
    parser.add_argument('movie_names', nargs='+', help='the movies need to be split')
    args = parser.parse_args()

    split_fasta(args.total_fasta, args.movie_names)


if __name__ == '__main__':
    main()
