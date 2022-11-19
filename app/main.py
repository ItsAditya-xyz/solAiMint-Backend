
from flask import Flask, request, url_for, redirect
import oauth2 as oauth
from flask_cors import CORS
import urllib.request
from flask_mysqldb import MySQL
from flask import Flask, request
import geocoder
import urllib.parse
import urllib.error
from decouple import config
import json
import requests
from decouple import config
from app.function import encrypt_message, decrypt_message, getSinglePost, mintPostHashAndTransfer, postContentOnAnonVoice, validateJWT
import time

application = Flask(__name__)
CORS(application)
application.debug = False

mysql = MySQL(application)


AI_KEY = config("AI_KEY")
SOLANA_PUBLIC_KEY = "FcEs1nSeFiF54gmYZNaTXau8gmhTBN4VBgSsJtGhZsLw"
BLOACKCHAIN_API_KEY_ID = config("BLOACKCHAIN_API_KEY_ID")
BLOCKCHAIN_API_SECRET_KEY = config("BLOCKCHAIN_API_SECRET_KEY")
SOLANA_SECRET_PHRASE = config("SOLANA_SECRET_PHRASE")



application.config.from_pyfile('config.cfg', silent=True)

oauth_store = {}



@application.route('/')
def hello():
    return {"status": "Live"}




@application.route('/request-art', methods=['POST'])
def requestArt():
    try:
        URL = "https://replicate.com/api/models/stability-ai/stable-diffusion/versions/8abccf52e7cba9f6e82317253f4a3549082e966db5584e92c808ece132037776/predictions"
        data = request.get_json()
        ip = None
        aiText = data['aiText']

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_KEY}"
        }

        payload = {"inputs": {"width": 512, "height": 512, "scheduler": "K-LMS", "num_outputs": "1",
                              "guidance_scale": 7.5, "prompt_strength": 0.8, "num_inference_steps": 50, "prompt": aiText}}
        res = requests.post(URL, json=payload, headers=headers)
        return {"status": True, "response": res.json(), "message": "Request successfully received.."}

    except:
        print(e)
        return {"status": False, "message": "Something went wrong. Please try again..."}


@application.route('/get-generated-art-by-id', methods=['POST'])
def getGeneratedArtById():
    try:
        data = request.get_json()
        id = data["uuid"]
        URL = f"https://replicate.com/api/models/stability-ai/stable-diffusion/versions/8abccf52e7cba9f6e82317253f4a3549082e966db5584e92c808ece132037776/predictions/{id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_KEY}"
        }
        res = requests.get(URL, headers=headers)
        return {"status": True, "response": res.json(), "message": "Request successfully received.."}
    except Exception as e:
        print(e)
        return {"status": False, "message": "Something went wrong. Please try again..."}


@application.route("/mint-solana-nft", methods=["POST"])
def mintSolanaNFT():
    resVal = None
    try:
        data = request.get_json()
        imageURL = data["imageURL"]
        nftName = data["nftName"]
        receiverPublicKey = data["receiverPublicKey"]
        shortName = nftName[:10]
        
        # code to mint this:
        payload = {
            "wait_for_confirmation": True,
            "wallet": {
                "secret_recovery_phrase": SOLANA_SECRET_PHRASE
            },
            "return_compiled_transaction": False,
            "name": shortName,
            "symbol": shortName[0:4],
            "description": "Buy this image of Super Musk!",
            "image_url": imageURL,
            "uri_metadata": {
                "animation_url": "https://www.arweave.net/efgh1234?ext=mp4",
                "attributes": [
                    {
                        "trait_type": "is_curious",
                        "value": "true"
                    },
                    {
                        "trait_type": "name",
                        "value": "george"
                    }
                ]
            },
            "upload_method": "S3",
            "is_mutable": True,
            "is_master_edition": True,
            "seller_fee_basis_points": 100,
            "creators": [
                SOLANA_PUBLIC_KEY
            ],
            "share": [
                100
            ],
            "network": "mainnet-beta"
        }

        headers = {
            "APIKeyID": BLOACKCHAIN_API_KEY_ID,
            "APISecretKey": BLOCKCHAIN_API_SECRET_KEY,
            "Content-Type": "application/json"

        }

        URL = "https://api.blockchainapi.com/v1/solana/nft"

        res = requests.post(URL, json=payload, headers=headers)
        resVal = res.json()
        mintToken = res.json()["mint"]

        payload = {"wallet": {
            "secret_recovery_phrase": SOLANA_SECRET_PHRASE
        },
            "token_address": mintToken,
            "sender_public_key": SOLANA_PUBLIC_KEY,
            "recipient_address": receiverPublicKey,
            "return_compiled_transaction": False,

            "network": "mainnet-beta"
        }

        headers = {
            "APIKeyID": KEY_ID,
            "APISecretKey": SECRET_KEY,
            "Content-Type": "application/json"

        }

        time.sleep(2)
        URL = "https://api.blockchainapi.com/v1/solana/wallet/transfer"

        res2 = requests.post(URL, json=payload, headers=headers)
        
        return {"status": True, "response": res2.json(), "message": "Minted Successfully"}

    except Exception as e:
        print(e)
        return {"status": False, "message": "Something went wrong. Please try again...", "response": resVal}


if __name__ == '__main__':
    application.run()
