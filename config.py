#!/usr/bin/env python

import logging
import sys
from configparser import ConfigParser
from pathlib import Path

logger = logging.getLogger("fdmr-mon")

def mk_config(cfg_file):

    CONF = {
        "GLOBAL": {},
        "FDMR_CXN": {},
        "OPB_FLTR": {},
        "FILES": {},
        "LOG": {},
        "WS": {}
        }
    
    default_values = {
        "LOCAL_SUB_FILE": "",
        "LOCAL_PEER_FILE": "",
        "LOCAL_TGID_FILE": ""
        }

    try:
        conf = ConfigParser(default_values)

        if not conf.read(cfg_file):
            sys.exit(f"Configuration file {cfg_file} is not a valid file.")

        for section in conf:
            if section == "GLOBAL":
                CONF["GLOBAL"] = {
                    "PR_INC": conf.getboolean(section, "HOMEBREW_INC", fallback=True),
                    "LH_ROWS": conf.getint(section, "LASTHEARD_ROWS", fallback=10),
                    "BRDG_INC": conf.getboolean(section, "BRIDGES_INC", fallback=False),
                    "EMPTY_MASTERS": conf.getboolean(section, "EMPTY_MASTERS", fallback=False),
                    "TGC_ROWS": conf.getint(section, "TGCOUNT_ROWS", fallback=20)
                    }
            elif section == "FDMR CONNECTION":
                CONF["FDMR_CXN"] = {
                    "FD_IP": conf.get(section, "FDMR_IP", fallback="127.0.0.1"),
                    "FD_PORT": conf.getint(section, "FDMR_PORT", fallback=4321),
                    }
            elif section == "OPB FILTER":
                CONF["OPB_FLTR"] = {
                    "OPB_FILTER": conf.get(section, "OPB_FILTER", fallback="").replace(" ", "").split(",")}
            elif section == "FILES":
                _path = conf[section]["FILES_PATH"]
                if not _path.endswith("/"):
                    _path = conf[section]["FILES_PATH"] = f"{_path}/"
                CONF["FILES"] = {
                    "PATH": conf.get(section, "FILES_PATH", fallback="./data/"),
                    "SUBS": conf.get(section, "SUBSCRIBER_FILE", fallback="local_subscriber_ids.csv"),
                    "PEER": conf.get(section, "PEER_FILE", fallback="rptrs.json"),
                    "TGID": conf.get(section, "TGID_FILE", fallback="UKtalkgroup_ids.json"),
                    "LCL_SUBS": conf.get(section, "LOCAL_SUB_FILE"),
                    "LCL_PEER": conf.get(section, "LOCAL_PEER_FILE"),
                    "LCL_TGID": conf.get(section, "LOCAL_TGID_FILE"),
                    "RELOAD_TIME": conf.getint(section, "RELOAD_TIME", fallback=7) * 864000,
                    "PEER_URL": conf.get(section, "PEER_URL"),
                    "SUBS_URL": conf.get(section, "SUBSCRIBER_URL"),
                    "TGID_URL": conf.get(section, "TGID_URL")
                    }
            elif section == "LOGGER":
                CONF["LOG"] = {
                    "PATH": conf.get(section, "LOG_PATH", fallback="./log"),
                    "LOG_FILE": conf.get(section, "LOG_FILE", fallback="FDMR-Monitor"),
                    "LOG_LEVEL": conf.get(section, "LOG_LEVEL", fallback="INFO"),
                    "P2F_LOG": Path(conf[section]["LOG_PATH"], conf[section]["LOG_FILE"])
                    }
            elif section == "WEBSOCKET SERVER":
                CONF["WS"] = {
                    "WS_PORT": conf.getint(section, "WEBSOCKET_PORT", fallback=9000),
                    "USE_SSL": conf.getboolean(section, "USE_SSL", fallback=False),
                    "SSL_PATH": conf.get(section, "SSL_PATH", fallback="./ssl"),
                    "SSL_CERT": conf.get(section, "SSL_CERTIFICATE", fallback="cert.pem"),
                    "P2F_CERT": Path(conf["WEBSOCKET SERVER"]["SSL_PATH"],
                                     conf["WEBSOCKET SERVER"]["SSL_CERTIFICATE"]),
                    "SSL_PKEY": conf.get(section, "SSL_PRIVATEKEY", fallback="key.pem"),
                    "P2F_PKEY": Path(conf["WEBSOCKET SERVER"]["SSL_PATH"],
                                     conf["WEBSOCKET SERVER"]["SSL_PRIVATEKEY"]),
                    "FREQ": conf.getint(section, "FREQUENCY", fallback=5),
                    "CLT_TO": conf.getint(section, "CLIENT_TIMEOUT", fallback=0)
                    }
            elif section == "DEFAULT":
                pass
            elif section == "DASHBOARD":
                pass

            else:
                logger.warning(f"Unrecognized section in config file: {section}.")

        return CONF

    except Exception as err:
        sys.exit(f"We found an error when parsing config file:\n{err}\n{type(err)}")
   


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    print(mk_config("mon.cfg"))

