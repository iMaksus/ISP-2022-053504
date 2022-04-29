import argparse
import os
import configparser
from ..serializator import create_serializer


class Converter():
    __parser = None


    def get_args(self):
        self.__parser = argparse.ArgumentParser(description="Configure serializing routes")
        self.__parser.add_argument("-src", dest="source", type=str, help="Source file path")
        self.__parser.add_argument("-dst", dest="destination", type=str, help="Destination file path")
        self.__parser.add_argument("-conf", dest="config", type=str, help="Get config file")


    def parse_args(self):
        args = self.__parser.parse_args()
        # args.source, args.destination, args.config = "data.toml", "data.yaml", "config.ini"
        # print(args.source)
        # print(args.destination)
        # print(args.config)
        if args.config:
            abs_conf_path = os.path.abspath(args.config)
            src_path, dst_path = self._get_config(abs_conf_path)
            print(src_path)
            print(dst_path)
        else:
            src_path, dst_path = args.source, args.destination
            print(src_path)
            print(dst_path)
        if src_path and dst_path:
            if os.path.exists(src_path) and os.path.isfile(src_path):
                abs_src_path = os.path.abspath(src_path)
                abs_dst_path = os.path.abspath(dst_path)
                self._serializing_parsing(abs_src_path, abs_dst_path)
            else:
                self.__parser.error(f"File {src_path} doesn't exist")
        else:
            self.__parser.error("Invalid arguments")


    def _get_config(self, config_path : str):
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)
            src_path = config['DEFAULT']['src_path'].replace('"','')
            dst_path = config['DEFAULT']['dst_path'].replace('"','')
            return src_path, dst_path
        else:
            self.__parser.error(f"File {config_path} doesn't exist")


    def _serializing_parsing(self, source_path : str, dest_path : str):
        ext_src = os.path.splitext(source_path)[1].replace('.','')
        ext_dst = os.path.splitext(dest_path)[1].replace('.','')
        if ext_src == ext_dst:
            print(f"Anable convert {ext_src} to {ext_dst} format")
            return None
        ser = create_serializer(ext_src)
        prs = create_serializer(ext_dst)
        if ser and prs:
            obj = ser.load(source_path)
            prs.dump(obj, dest_path)
        else:
            print(f"Anable convert {ext_src} to {ext_dst} format")
            return None