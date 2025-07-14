# Reviewed by Tyler. Sage to use.

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
# noinspection HttpUrlsUsage
class BlockEngine:
    # Reviewed by Tyler. https://jito-labs.gitbook.io/mev/searcher-resources/block-engine/mainnet-addresses
    MAINNET_ADDRESS = {
        "Mainnet": {
            "block_engine_url": "https://mainnet.block-engine.jito.wtf",
        },
        "Amsterdam": {
            "block_engine_url": "https://amsterdam.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "74.118.140.240:1002",
            "relayer_url": "http://amsterdam.mainnet.relayer.jito.wtf:8100",
        },
        "Frankfurt": {
            "block_engine_url": "https://frankfurt.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "145.40.93.84:1002",
            "relayer_url": "http://frankfurt.mainnet.relayer.jito.wtf:8100",
        },
        "New York": {
            "block_engine_url": "https://ny.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "141.98.216.96:1002",
            "relayer_url": "http://ny.mainnet.relayer.jito.wtf:8100",
        },
        "Tokyo": {
            "block_engine_url": "https://tokyo.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "202.8.9.160:1002",
            "relayer_url": "http://tokyo.mainnet.relayer.jito.wtf:8100",
        },
        "Salt Lake City": {
            "block_engine_url": "https://slc.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "64.130.53.8:1002",
            "relayer_url": "http://slc.mainnet.relayer.jito.wtf:8100"
        }

    }

    # Reviewed by Tyler. https://jito-labs.gitbook.io/mev/searcher-resources/block-engine/testnet-addresses
    TESTNET_ADDRESS = {
        "Dallas": {
            "block_engine_url": "https://dallas.testnet.block-engine.jito.wtf",
            "shred_receiver_addr": "141.98.218.45:1002",  # "147.28.154.132:1002",
            "relayer_url": "http://dallas.testnet.relayer.jito.wtf:8100",
        },

        "New York": {
            "block_engine_url": "https://ny.testnet.block-engine.jito.wtf",
            "shred_receiver_addr": "141.98.216.132:1002",  # "141.98.216.97:1002",
            "relayer_url": "http://ny.testnet.relayer.jito.wtf:8100"  # "http://nyc.testnet.relayer.jito.wtf:8100",
        },

    }

    # noinspection HttpUrlsUsage
    @staticmethod
    def get_block_engines(network="mainnet") -> dict | None:
        if network == "mainnet":
            return BlockEngine.MAINNET_ADDRESS
        if network == "testnet":
            return BlockEngine.TESTNET_ADDRESS
        return None
