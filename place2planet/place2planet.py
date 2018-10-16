#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import glob
import sys
import subprocess
from place2geojson import search
from place2footprint import fp
from place2eeintersect import eefp
from os import linesep
import textwrap as _textwrap
from argparse import RawTextHelpFormatter
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path=os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path)

def planet_key_entry(args):
    if args.type=="quiet":
        write_planet_json({'key': args.key})
    elif args.type==None and args.key==None:
        try:
            subprocess.call('planet init',shell=True)
        except Exception as e:
            print('Failed to Initialize')

def eeinit():
    subprocess.call('earthengine authenticate', shell=True)
def eeinit_from_parser(args):
    eeinit()

def refresh():
    filelist = glob.glob(os.path.join(path, "*.csv"))
    for f in filelist:
        os.remove(f)
    subprocess.call('python ee_rep.py', shell=True)
    subprocess.call('python gitcl.py', shell=True)


def refresh_from_parser(args):
    refresh()

def search_from_parser(args):
    search(place=args.place,
           local=args.local)


def footprint_from_parser(args):
    fp(place=args.place,
        item=args.item,
        local=args.local,
        start=args.start,
        end=args.end)

def intersect_from_parser(args):
    eefp(place=args.place,
        op=args.operator,
        local=args.local,
        start=args.start,
        end=args.end)

spacing = '                               '

def main(args=None):
    parser = argparse.ArgumentParser(description='Hacktober 2018 Place to Planet & EE CLI')

    subparsers = parser.add_subparsers()
    parser_planet_key = subparsers.add_parser('planetkey', help='Setting up planet API Key')
    optional_named = parser_planet_key.add_argument_group('Optional named arguments')
    optional_named.add_argument('--type', help='For direct key entry type --type quiet')
    optional_named.add_argument('--key', help='Your Planet API Key')
    parser_planet_key.set_defaults(func=planet_key_entry)

    parser_eeinit = subparsers.add_parser('eeinit',help='''Initialize Google Earth Engine''')
    parser_eeinit.set_defaults(func=eeinit_from_parser)

    parser_refresh = subparsers.add_parser('refresh',help='Refreshes your personal asset list and GEE Asset list')
    parser_refresh.set_defaults(func=refresh_from_parser)

    parser_search = subparsers.add_parser('search',help='Search for a place and export as a GeoJSON')
    parser_search.add_argument('--place',help='Search for a place in the form ex: "Raleigh" or "Raleigh,NC" try both to see what happens')
    parser_search.add_argument('--local',help='Full path of the geojson file to be exported')
    parser_search.set_defaults(func=search_from_parser)

    parser_footprint = subparsers.add_parser('footprint',help='Use a place search to find assets and export footprint as GeoJSON')
    parser_footprint.add_argument('--place',help='Search for a place in the form ex: "Raleigh" or "Raleigh,NC" try both to see what happens')
    parser_footprint.add_argument('--item',help='Planet item type example PSScene4Band or PSOrthoTile and so on')
    parser_footprint.add_argument('--start',help='Start Date in the format YYYY-MM-DD')
    parser_footprint.add_argument('--end',help='End Date in the format YYYY-MM-DD')
    parser_footprint.add_argument('--local',help='Full path of the footprint geojson file to be exported')
    parser_footprint.set_defaults(func=footprint_from_parser)

    parser_intersect = subparsers.add_parser('intersect',help='Use a place search to find assets and export assets from Earth Engine that intersect as CSV report')
    parser_intersect.add_argument('--place',help='Search for a place in the form ex: "Raleigh" or "Raleigh,NC" try both to see what happens')
    parser_intersect.add_argument('--start',help='Start Date in the format YYYY-MM-DD')
    parser_intersect.add_argument('--end',help='End Date in the format YYYY-MM-DD')
    parser_intersect.add_argument('--local',help='Full path of the footprint geojson file to be exported')
    optional_named = parser_intersect.add_argument_group('Optional named arguments for geometry only')
    optional_named.add_argument('--operator',help='Use bb for Bounding box incase the geometry is complex or has too many vertices', default=None)
    parser_intersect.set_defaults(func=intersect_from_parser)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
