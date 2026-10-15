# MAKI WIND STUDIO v11.11.24 — Sade Veri ve Kalite Özeti
import datetime
import hashlib
import io
import math
import base64
import os
import re
import json
import subprocess
import shutil
import glob
import gzip
import urllib.parse
import urllib.request
import urllib.error
import time
import pickle
import uuid
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


MAKI_LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAASUAAABKCAYAAAD9skJMAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAACRJSURBVHhe7Z13fB3Vnei/Z+ZWlStLlmUVV4yxcaMY24BpCSEhS7IpJLvJwm5YSCCfvCxLOiR5L9l9CeElWfZlKckmJCTA8mBpgdDBNsXGGNtY2LJly7Zk9a57pdvvnZnz/pi5VVfuAkmer3ysq5kzp5/f/M7vlCv8I3GJzclH5F84CsajJo4nHTY2eYj3sSEp+RdsbGxsPkiErSkdJ+Px4hiPmhiPdNpMGt5PDedkYWtKNjY2EwpbKB0Pk+/lY2MzaZj6wzdbgNhMEibjUGs8sDUlGxubCYUtlGxsbCYUtlCysbGZUNhCycbGZkJxShm6hdSRQs2+azPFsY3Hk49TSlNS/bvyL9nY2EwwThmhJBIBXC2P5F+2sbGZYJwyQsnZuwlloB5hJPNv2djYTCBOGaGk9mxASQYQ0Z78WzY2NhOIsYWSOIKbZKj+RtCitl1pCpDfFMd2k7Ch2qAUqMmjEzr5/ieqA5ASJRkAPYazf3NeRmwmCuIof0ZX8ljOZlzIL+aT7MbWlKYSQmC4KxFGAmWwHsUewtnYTFhODaEE6NPPRkhQIz04utaBnNrLs2xsJiunjFBKzvo4UnVC0o+zZz1KrDffi43N1KPA8OiE3TgzpYWSIZPp4xz16eehVZ0Pho46tBtH16v28gAbmwnIlBVKCS1EMNGHbiQAkIqDxKKvIr01KPF+HB0vogw35T9mc5TkG5+P7Wf0y9d8ActxcJOI/AI5GW4SMmWFUmd4F+FkHyIri9r0c4kvvgnDUYTDX4+r/S+I+FDOczZHZpK2dZtJwpQUSpoepS24hYgWRCiO9HWpuEnM/mviC28AaeBqfRJnz5v2MM7mg8eW9GmmpFDqiuxiINqEQ3FZgwULIZCuaSTO+EcSZ3wFqYdxNf4Hin8PSCM7CBubw5M/TDpRZ5NmygklzYjTOrKFwWg7DsWVf9sUTM4y4ou/RmLxzSjxAEW7bkeJdOf7tLGx+QCYUkJJIumL7KNleBNuRxEO4c73kkaqbmKLvkL87O8jE8N43vsJSqwv39uEJd90fPw/o1/aR3IppJTEEhoDgSiDeS4UMScYjo38mEwnJUg5+vrRuXFgnIK1MRH+4NQ55E0zorzb9yjrW3/JrNJz+ei8H1BVtCh935AGCX0El+pDERl57OjbgrvpP5Hu6cSX3IxeNAvExG15pig5WRxP9Zvx67rB1oYeHnq6MbejSjh3aRXXX70862I+heLNzZduSHoGQrR2BhEK1FWVUFdViqqezPwfBx9w9FOdKaMpSSkJxDvZO/QyukyiCgdK/imT0mAg2kJX6D0MQ0tf1qrWEF35M6SzFNf++1FG9o/RaWyyMYD2riDPbmjm2fXN5u8NzTz7WjPbGk5scaqUkrd2dPLz323jyz94mRt/+Aq3/2YLb9V3oem2/W8qM2WEkiGTtAW30RXahRCgKCoiSxsCEIpKqWsmzcMb2et/kYQeyTzvnUlsxffRyxbj7H4VdWinLZjGJGsNkEgplRIhJUKCOAlLhJo7hvmPB3bw7IaDRGNJQuEEr2xs5d6H69nX4s/3bjOFmDJCKZL00zDwZwxp2jIMaSDz9rcJBKWuKmaVnM2ewefY0fcokWRmnZJUHCTmfha9cg2O4b04+rfZe+SOEiFS0kkiT1QiAVvquznYFsAwZFrAGVKyr3mIHbtPTAuzmdhMCaEkMWgNbqYr1JB1TUdKPccfgCIczCpdyazSlbzb9zBvd99HKNGf5cGBNv1stKoLUcJtOHo3gTE6nA+WE+/044YQpoA6ZnKfCQTjmWFa1q14QiccG+d1ZeNsJ7c5PFNCKBmGxtaeB80tJVZ/1WUcQ2bsRtm41CKWVFxFbfFytvU+zCttPyWcGMx4ECp6UR1a7eUowWYcvW8g8sLKn8M6tp/cdn+sziQ1RjpRdzyYKcmkxcIK7uhCLZyrFGcuqKDIk1n4mqKy3MOs6tL8y2OTH83RuCM9bzOuTAmhtD+wgW5LS5JWo4kkh0ka8VyPWfjcNZxT9bdUuGezZ+AFHm26kaQezngQCoZrGskFf4NjcCvOzlcRcpzf0JMUU7xJpDAN1Ecrlg7Hpatm86Hz56Cq1pIAwOFUWXtuHZefPzvfu80UYtILJUMm2NR5L1KYdg1h9YeEFkQzovnec5jjW8PSyr/G6yijO7SLX793JcOJ9hybiFQ8xJf8E2rXyziaH0FoodSdAu5UoUB+pUBIaaoSqTfDCaAogtu/eTH3/OgjLDqtgqWnT+f2b1zET265CI/bmfGYr8XkO5tJx0kVSh9EW9jvX093eA8iZQ9NaUpagJg2jCQzfSylwUi8B3/sEMFED+HkAIsqPkJl0XwECsFELw/uvpauUL117In1nOIlvuI2XO0v4Gm8CyVmn1yZjVnnKSF18oSzAD520Txe+v3VPPfbz/L5K89AUd7P1mXzQXBShdL7TUIP807PA6Z1w/yXRjMSDCe60LKGcLqMs2fwOZ45+D1ePPRj1rX9nI0d9zAc77amtQUjiR6eOfAdmoc3pWfyAAzPDOLLv42j7Rk87/0MNbgvfW8yI6W0Vkynhl7HR/YLwcbmRDjuFd3H0/6OK6LDsGfwOZ5t+QGaFh2VIClhxYzP8OE536bEWZm6ylCsnS3df2B/YD0jcUvjESAQuNQSipzlBBO9THPVcensb7Kw4jIcZPbQuRvvwb3739GqLya25J8xKs7KKo3CpTI0HKO1aySv0wtKip2cMXcaAOGYRuPBIZrbAkTjGl63wxq2VOBQR787BgMx6hv76OgNkdQMfMUuFi+oYMmC6QX9ZyMlDAQibNvVQ1d/BCOdLkmFz8OH1syh3OdmaDhGW1cwr+YEvlInC2aXo+kGT72yn+/+/A2kzOReAn916Xzu/fFHsp4ziyeW0DnUMUw0Wtg+J4Rgdk0JxV4XB9sDJBK5M59ej5O6mcWUloy9hchmcjNphVJCD/LkgVtoGX4LOcYO/xneM7j6jF8x3XNazvVI0s+B4dfZ3vsw3eGdGIYBQlDkKOfKeT8iqgdI6jHKPXOY51uDWy1JPysSfko2fA7CHeiV5xNfejP69JWpu2l/2byxrYO7/6ueZHYHE+YM04++fiGbtnfyyqZW9hwcpLl9mHhcw+1xsGheOcsWzuCvLpvH6uXVAISiGuvfbmXD2+3s2NNHZ28IXZMUlzg587QKLj63jisvnc/CueWZuLKIxjU2bGnlxTda2dbQQ3dfOC1QpIBpPjdXXDiXtStr8bgc/PbRneZSrSyJs/qsGm67cXWOUErdS/HxAkIpEtN46pX9PP96C5ECQklRBBeeU8cXP7GIRELn/9y3jZ7+lA3PZG6dj+s/u5QVZ1blXJ+KSGR6jjP781RHvfX7//PH+RePhuMpnuN5Ziz2Db3KzoGniOshhGXRyA8/ZgSZV3Yh5e45Oau7naqX6d4F1BQvJaoNM5zoRMokupFkru8CVs78AnUlZ1PunYMqnLkrw1UvIjmCo3cjItaDEu3GKJmP9NZk/GQhpaS+sZ+HntlDZ2+InoGw6frDOFWFjt4Q9z/ewMbtXfT0h0kmdQxDkkjodPWGqG/sp+mQn7JSN1UVxTz+wj7uefg9tu7sJTASNxcXAomETmdPiPf29ROMJDhjXjnTfJ6ctCQ0nXsequf3jzXwzs4eQhFTMAhhFp4A4jGdvc1D7GoaYNf+Ad7b20+vld6efjPtFdM8fPJDCzCkZG/zEK9sajUjsMKRAhbOLeeqyzIvg0g0yeMvN3Hvw/XsOTBohpnlBvxRTptTzrWfOpP5s8vo7gtx/5O7aGrx5/gDWHN2DXNqfemwpxpSGrzb+zBvd93HnoHnaBx8HkU4qSxaQCQ5xHv9j7G583c0Dj7PnsHnqCw6nWLn9AI9YHJyeD1/DMysWy3wGN2J/WRCml22klUzr8WheiFr6JCNrsdpCWwqsDRA4BAuaouXc8W8H3B+zfU41WIMNLb0/J6BaAtCCFQK7J8DkrOuAqEg9Dhq32ZcTfehBA/me8uQ6vVZSAmNh/w8+OcGWjqGATlqD7AQAiGgoWmAux+s566HdvCbR3bS3h0saP8RAqIxjZc2trJhSzu6YeQU/+8e3ckfn9pNe1dwVFxphLlyuqMnxO6mwVHlOjrWAqQ8WfFGYxqPv9zEXQ/W090XHhWm6lC4eNUs/uXrF7D8jMrM8LNAIkdfmYII6Inspsn/Knv9L9Pof5nBWAtYR/N0hxvY63/ZdEMvEU4OHl29TBKOWihlC4SJQKlzJmtqb+C6Jf8Ph+rJbAfJqh0hBHuGnieuBzMXcxD4nNVcWPdVrjrtJyjCwXC8k7e6fo0xxpAQwPBUYZTOAUDREzg6X8bV+gQicYQ9WTlpg1g0STiiIa1bYzUsQ5fsaxniwacb6R8y9+vl+M97MBiM825DL919mXVX7+7p5a6HdhAMJXIqsYBsM5EgLS0sP/yxkFaismVJLK7x1Kv7+cV92+gfioxqP0IRXLyyjn+79VLmzS7LnV2T5pTqmGmc4oy5XSfnsvmynkoo2cLmcG402V3p/XLWJwlY2k510RKuX/5YWmPKXyITTgzQMPh07kUrrNRnp3CztOIqrlv6KEKotIxsoWXkzSw/KazSUFSM4nlghSSMJM4Df0Id3H7YEyxzYrX+KPI6ue7TS3nirk/yw6+tYW6tDyHI3UEmwDAk8XgSr9fJh8+fwz9dew5nLZ6Bw6mm8ywxZ9IA2nqC9A1FQJrP3vmH7cTielpgWP0dIUBRBW6Xg5mVxfhKXDhUgcgSDql0ZIzZhVsE6QWU5l+JhM7Trx7gf/3qLYJh6wscrHvSsiF9dO1cfve/P0p5maeQYpROY+rzqYIQCkI4UBQHquJIl4G5x1BBUcx7hTaejwf58mA8nZL758RGSklrxOClnjiNIxpBzey4lZ7Tueq0n+J0FI/OhYC3O/9AWMvXYuSoZl5bvJxrFt+PwGBH72PE9VwjawohFHBPN/+Q5n8iGcZ98CGUeKHNoobpMbWyU0oEEkWBW647lx/ffCErl1Zzw9Ur+Mb1K6mdaRnWZUpNMJ+rmVnCv/zTBdz3k4/yrevP48m7P8UnLpuf1i4EIKw4wuEk0bi5NWZv8xA79vRZ0acWdJm7+ivLvfz0G2vZ/tS1bH7073j3z//Ai3/4HKtXVKM6FFMomKnJFRqjCtoablpSJ540eOKlJr5/55tommGmTUozfVJS7HXwt1ct4p4fXY7DOXanEsisoerRiSVTOGsk9BAxfYSEHsYosA8yhfkCSL0GzDgkBgk9TNwIYchkweFyColEM2LEtRESehBNjx3Gf3Zsph9DauZzRsysFwSX1N3CjSue4aYVz3HTiuc4t+pvACh2zeDyud9OX7/prOepLTlrTH0pv8Mfr3s/OW5D9wdB1BD8pSvC/S1hXu6O4U9Kqr0q5U6FaZ5ZIA26w7tzFj6CIGnEiGsB5pddhCpG76fKpsRVRYVnLs3DG3EpJVQVL8qqcPO3kBqO7g2ogT3Zl1Einegz1mCUzMvpwftahnj1rTYM3RqOWA95vE5++d1L8HrMFcpCgMelsnVXL509oZxmoSiwekU1X7vmHLxuMw+KEPhKXDy97iCGYVinM5rCYVqZm8tWz2ZurY9nX2vm9a0d6DnnEAlKS93cct25fP5ji/B6nKbWJATlPg9nnTmDhv2DdPeGzCRISzwJWDBnGp/88AIMI9fQbXZEAUIyNBzjpTcPYRhYHd20CkqgsryIf/j0Ur77ldU4naNtdgD9gxGee62ZkWDCKgMzjBkVXi5ZNWsMQ7ckkvTTG95NW3A7jYMvcCDwGr2RRuL6CNFkAJdahFPJTAAMx9vpCe/GH2slEGvF7fARSQ7RHtzO3sEXOTj8JuHkIA7FhcdRgsiyMRpSIxBvoyu4k5aRTTQOvkDryDsMxdtIGmHiWpAi5/S0JqMbcfqj++kLNxKItTMS78TrLONg4HV2DTxNIN5BkbMCj8PHcKKTkUQPMW2EmDaCU/HicZRhGElG4j2MxLuJaSPEtRGKHRU4VE9BwTT6ysRnAgulXFktEewPajzTFWMgJjEQHAzrHAprzClyUO31UO6ZQyjRx0DsIAbW29kKqi+6l+meuVR5F1mNJDf8lFOEeeaSZkTpjeyltnQZLqUkp3qFkcTZ9jRKsNnaEW/dkwY4y9Cr10KW8NvXEuDVt9pMoWBth0HA7OpSvvqFszK76gU4HSrrNrfR3DGM6U0iAJfLwdpz6rjykvk5SXY5Vf701B503dJChNk0K8o8XLZmNnPrfDz+YhMN+wfM4VfWLv7zls3ki584k5qqkpwwhYASr4tYQmPj9k5LHplGd0FhoSSlTBvmQRBP6BjSFGap6xJJRZmX6z+3jOs/v5wib9Z2kTzSQimUNOO1yq2yfGyhNBzv4O3u+1nX9gv2DDxLe/BdukMNtI1spXHoRfYMvQgYTHPPxuMwn3+39xFeOPQvvNf/BA0Dz+B1+KjvfZyNXfdwaPhtOkP1HAhsoC/cRHXxEopdMxAIDKnTHHiT1zv+g7e6fst+/wa6QrvoDL1Hc+BNdg88S+vIFopd05nunYcQKqFEH6+13clrHf9Ow8AzNAXWIVB5qeVfaQ++S29kL9Pcs6kuPpPX2u9kfdvP2TXwZ3YNPEOJcwZzfOcRTg7xVtdvebX1ZzQMPMOugT+zYNollHtmjZoMyrTYycXYevMEI6IZ1AeStIT0TIlLaAgk+fXBEPWBJD5XLatqvsTs0vNyjrsVgGHovNl5D80jG484DHCrJZxR/hEcipf24PbRqrg0ENHMFw2kDjUTgDK8G7JOtRwLAZT7PBmBZOFQRe5xr0IghcDpVPEVWDBYZGk4JoWbYSiSyLEWS0yvVRVeKspGhwngdqvUVRXjtQRH4ZAzZOcju0Nkv72FELicKuU+D46jOtLW9JPSLA+HbiR4o+Metnb/ibg+gsPhYX7Zhayq/ntm+1aiCicJPcTm7j+wpfv+zAF/IneDzPae/2Kv/2V0qaVfOFIatAe30jy8kaRmPtcbbmR92y9oHt6ELpP43DUsq/xrzpn5BXzuaiSSgWgzr7bewcHAxkwE1m9pHd+8ufs+a2gpmOFdwLyy1Zan3EdyyboqC+lHk5sJKpRyi1lKSVdMZ+NAHC27lgRIIdg3ovHHljA7AklmFi3mgtovU128JMuj2SEC8Q7e7Lib5pFNY1Z3imnuOqqKTqc/0kRUz7NH6TGU4KHMfq+U9oNAxP1HDBtTgcjtmNZHIQSKktvQUl1TKdCRhWUVTP+d9TmF25k7ZDVTai5mjMYK21p03SAS00km9Zwwj5wz049MfchLUM9gmN89tpMXXj905GNtU2WSf70ArSPv0DDwLIa113FOyXl8eM63uGzON7hi7m1Mc9eBNIXXgeENdIV3pp/NhC8ZTvRyXvW1fGj2t5jruyDrjqQvvBdNmpu8t3TfT19kPwIockxjxYzPcPnc73L5nG+xuvpLOBQ3QgjCyQHq+x4jkT0DbEWoGxpJPcKFdTfysfnfZ3XtdZS56rK9HFXej6ZOJhMTQCiluki2yyVmSLb7kxwK5U6fpxq+FIKmEY0HWiLUByRzfatZW3MTld4FOZ6lYdAdbuC19v/LPv8rY64EB1CEk3L3HIKJXvyxQ7n3hvcgkqYR3DSqWiZLKcFRbOahQHak5cVUWjICrUCW0+TZusfE9GftY8vzXl1VnGOkToXZeHCIg22BgkEPDcd5571u4lmr0OUYSU3li3RaJWefOYMFc8uy8mumDwktHSPc+cdtPLehOT+oDCITXnbexmLv0MvoRhwBKMLFjKKFlLpnoukxfO5aKr0LzeGNhGhymM7gjvwgQMLMokVcUvd11tR8ibOrrkYVrnR5xvQQujQN4AeGX08/VuycTlXRGShCNRfglp2PghMpwZA6/lgbg1HL7iascrTqab7vAtbW3cTKmddw2rSL0uvi8uswn+z7hepkMjMBhNKRCSQM1vXEMZVcs9Gn+7zV/3UE+0aS/OlQmPqAYEH5ZXx4zrcp89alZzmwDoTrCTXwSusdvNPzR2L6SHZUOThVL/5YJwPR5pzZG2fXesDqJOn5eDMW3bcQsr6VN4N5fnWK/GFbIeQYi0LzkWnZlrEpZHPWohmoqpLu4Kn7Xf1hHnxmDwdb/TlD1FhM4y/rDvDsa81WeWcEy2FJeQaqK4v55a2XMbvGtFeZacxogB3dIX5y75bDC6acbpmfq1yGoi2mHwlSauzsf4oHdl/DA3u+yAO7v0hLcHOqkEgacYbjnTntIsWMooUUuypxKF5KnZU4VTdYE6emJROimp+4Nmw2PsAf7+CV1jt4YPcXeGDPF3ly/80kZTj9IkjIKMFk3qysdW9h+WV4VB+qcKKSa2PLKs5RZNfzGF4mLScglFLFciyuECmZX7hoNQmbBhO0RjRID5jM36aWknmLasDekSR37w+zeQAWTPsQV59+F2We2pwpWIlBINbO+vY7eWTfl2kLvlPg6FxJVBsmlOihN9JIVAuAMGfenB0vmPlJG6IzzUOruQyp5BtwrXiFtWrbMvqORXZJSay2P1bxZSHJSJxs7xecU0tFgXVAum7w5rZOvnTri/zsN1t47e12nnipiWu+8zx3/G4roXDCFEYpQ3Pu42lyrluJVYTgrEUz+MX3LmXm9KIcz8L63e+P8IN/38iLb5irlQuTWemen/5shKKky8mQOlFtmECsC3+si0Csi6QWQ+BA4LDsjaaASWPl0yncpIrbFKKFIzWFuKnuaHqCSHIQf9yMbzjWA1JJxyckGIa5TktgPSYBKZlelLsvM4exm0gmjPzynwIoZs7HFgofNCFN5+nOaFojSTXodJKzZpzMawpdEYM7m0I82RHD61rCPy59ktMrLsWpejNiWAh0I0HHyA7+q/FL3Lvzo6zv+DfaQlvxx1vZ63+RjZ13MxBtwR9rI2GEAImj62VEpCfdEGRWbzUqVqBPPwcKbE3BauTmb0t3PwLpTngUftPf1ViAIq+D669eZi6ItPylki0Ng87uEL/971186dYX+NbPXmd7Qy+JpG5qpMLsPCkKJUWm02ppsFY6FEVw3rJqfvqNi6mpKs5ZkJmaVQwEY/z4rs289OYhNG30cNrUKI+sMtYUnZn+rCpu1tZ9le+true2NQ3ctmYX3171Dt9atYVvr9rKN1du4cp5/5pbYGlhmR9R1lDcotRVRbGr0hQMAmYWL+RvF/+G21Y3cNuaBr67aocV1xa+s2obN614nsUVH4OsskoFp4r8F5iJOEKdmocapv/KvTnJOQFN6f1hXW+cnqi1h8tCpCpWZL3LUpVkubBm8PvmMP+2d4TWiI8r59/DVQtup8q7GI9alg4Da3o3EGvnrY7/5MHd1/Lr+o/xRNMtdAR3IAQk9Ci6kUToCZz7HwRrOIIVtwSks4T4gmuQnpmZhKbJb1mHUTvymlg6T0dod/ne8r3//aeWsPbcOhTF0jLTgiY1jW/lJqsPylQ4WR21ULLNa4VtPg6HwiWr6vjODauprio2wzIDtXwIegfD/OK+razb3JZjw8rEa5VzgfBTLKn8BC6HuehUlwlaR96hZXgT/ngrXaGdPLn/Fh7b+1WeO/gDtvY8QEg7toP6sqNWhYvllZ9Kp2so1kqTfz390SaGYod4b+C/eXTvV3ii6WbWtf2cfX7zuwgzJZVVYWMgD387p34OUyyTknFc0Z1VZKkvA8uO6ijdut746JfXYclUky4Fbw8l+V8NIzx0KElcXMElc+/lwllfZ75vLRXueTgdnvQTqbe9xMgM9aSkyFmOQ3Hj6HsLdWhHVvKs5uBwo836OHr1JUh19BS7mfy0JLOSeEyZOixWsg87Pex2O7j9GxexZkUNLpcjnaoUlsKZtnuVFLuYO6ssx8/hhAJY658K+HG5VD5+8Vy+9ndnmxpTlj8hzQXvB9sD/OpP77Lh7XaisQJLKrKUpUJ5rCpawsqqL+JSSwBJZ2gHfzl4G480foVH9t7IgcAbHAq+Q1NgPf54O2418+UDOUkelX7zQn6ca+qup853NiBIGnHq+x7n0X038sjeL/NK289pD77LwcAmmoc3oqObGlFa4GciGbvGxiDLeyqsYw5jgjP+mtIJltfiUic1HpUKp6DCpVDuUih3Ws6lMM0pKHMqlDkVfE6FMqeKz6FQ6lAodQh8DjOL6/ri3L0/zLPdZQT5PPNm3MHy6ls5p+o6VlR+ijPKL6WmeDnT3HUUOcpxKh7cjhJqSpZxRsUVlODEefAhhJFaYWy2VykcaJWriS+4FsNrnnk0GomiCFSHgqoqqA4Fh0MpOMUPpnBwqJZfVUFVzN8FhbMkHabqyPhVlNFfdTSrppSffvMi/ubKhZw2uwxhrdGRmFmSAIpgTl0p131mKZ/72Bk56XBY6c/eNCuEyEljKo/5efN6nXz68gV8+XPLqK4qyqQ1VSaKwv5WP//5yHts2t5FPGGgKlbYWflTlNSQLhdFKFxQewOra65jVsm5uJVSoloAf7yduB7Eq5Yxu3Qlq6r/nktn3YxbNQWux1GCz1mFz1mNz1VDkTNzDpWquvE5Z1LmrMbnrKbYUZ5e/1aqzuDKeT9kWeUnqPTMBwQjsV4C8U6kNPC5alk0/XIunvU/WFb5SYRQUBSVImcFPlcNPmc1Za4aVGX0S8y0kY4eygIoqBSp08z0OqvxuWtQFVcBYTp5EYHjPOTtiNKm4O3sqAp6GMVgXGffiEbU2rFuGl7znpVgWG8MAWmTdvabPbXhXQhwKjDNqVDtcTDdrYOMEEn6CScHCScHSBhhknoUVTiZ7j2NmcWLKW5/EU/97YiE34oDEAr69JXElv0z+ow1Oau4U0gJB9sCvLalfdS6nJqqEj51+YKca5pusH5zOy3tuVP1LqfC8kUzWGUd9pYimTR44M+7SebZY6aVeli7sobZNbkrn6U07Tjbdvayc18/PQNh+oeiaJpBZYWX6spizj6zirUra+noDvH61vac5wHm1ZVx5SXzMAzJ/lY/G94e7WfBnGlcsXZu/mWC4QTrN7fRMxAZvSjVskMtPX06c+t8vLG1k5FQ7rEzldO8XHBOLXXVmYP3sknqUQZiTfSG9xPV/OhSQxVOvI4yqooXU+VdiCNrm8lg9CCD0WYMzGFjmWsWtSXLAAgnB2kP7kBiam7Fzkpqipelt6lIDMLaED0hc5tKakGmQ/Xgc9ZQU7KUMldteptJUsboDTcSTGRm4uaUrrLOQsoQ0YZ4tvmH7B9al56guWLOrZxfewOajNMfbiKQ6LR8S+b4VlPkqJgyGtNxCqW8zB91WaSiOuoHJgRq6BDu7T/E2fc2SN2a5VLRp59DfNk30StXFZhxy2AcZo2NWuAgfMMoPDenpLdx5KKnJG4e+Ysws5FSEo1qBCNJgpEEum5QWuTCV+KiuNhlCl4p08I8G2GFzVH6yWes/KWRoCiZF0n+vZwV74fBkHr6+D8hlHHttOZMsCnYzLVGxx6Xgc6BwOvU9z1BZ3AH4eQAWGFfddpP05typzq2UDoCwkji2nMXrgP3oySsBZNCoM24gNiK72FMWzLGuiSbicDkaWkQ0fy82XEP23oezFkyIqXBDSuepLZ4RY7/qcox2pTE6Go+plov8PwEx9G7EWfnSyjJkDkkxCA559NEV/8So3zZKSuQUjU50d1kIpL0MxRrxZCGZVeSGNJg+YzPUF28NN/7ySe/8D4gd4yakij48ejJjuq4AijAeIRpooQ7cO+8A2f7c6YSrbiIn/1DEguuGXMt0qnAyS1lmxQJI0pveA99kb2EEv0oiou64hXMLTv/iEfunDATqFKPQSidqEBinATIeIQJJMO4DvwJd+Pdpn5Uejrxs76PNmONuQv2FOYklrLNRGECVaoIhBJZg9ece6NIGVmP4O0wjJMAOcm2KmEkUbs34Nl5B+hRtFkfJ7nwH9GL6k55gcRJK2WbCcUEqlRbKOUjDdThvbh2/wphJNDmfpZk7WVIR2ax3anOSShlm4nGBKrUXKF0BLLTfdQP5TDxhZISH8LR+iRCj6PVfRS9dMGk0I5OJOfHWpcnEpfNBGUCVaoIhDI2pRNdx3Hkxj2WjxOL92SGq0Y6IdqLUbYY6cja3Z7HsYecS6EUn2iYJ4tCactmoqRzyvF+FewJ6wbH9VAWh29hE0QopTje+A8X7rGFKfQ4UnGNXjWex+HvHplCKT7RME8WhdKWzURJ55Tj/SrYCS6UxnFD7sQhO4dHcqjmMab51/OdjY3N+JDzZZRTkamaLxubqcpJteDmaxPH6mxsTlnezw6Qiuv9jPMYEMPHMPt2ckhFdzJLZDzCtJly2M3jJHGiBVlI5GTCPKma0pEplJgTZTzCtLGx+aB4n4WSjY2NzeGZ8F8cYDOFyDci5jubSUK2zDgeV4jMfVtTsrGxmVD8f02DuxcNvpNkAAAAAElFTkSuQmCC"
MAKI_LOGO_DATA_URI = f"data:image/png;base64,{MAKI_LOGO_B64}"


# ============================================================
# SAYFA AYARLARI
# ============================================================

st.set_page_config(
    page_title="Maki Wind Studio",
    layout="wide"
)


# ============================================================
# UYGULAMA STATE YONETIMI
# ============================================================
# ÖNEMLİ: file_uploader widget değerleri doğrudan session_state'e
# yazılmaz. Dosyanın adı ve bytes içeriği ayrı app_state alanında saklanır.

class KayitliDosya:
    """UploadedFile benzeri dosya nesnesi; bytes veya yerel dosya yolu kullanabilir."""

    def __init__(self, name, data=None, mime_type=None, source_path=None, size=None):
        self.name = name
        self._data = data
        self.source_path = source_path
        self.type = mime_type
        self.size = int(size if size is not None else (len(data) if data is not None else 0))

    def getvalue(self):
        if self._data is not None:
            return self._data
        if self.source_path:
            return Path(self.source_path).read_bytes()
        return b""

    def read(self):
        return self.getvalue()


APP_STATE_DEFAULTS = {
    "wind_data_files": [],
    "active_wind_data": None,
    "date_start": None,
    "date_end": None,
    "mast_coordinates": {},
    "selected_masts": [],
    "selected_wind_data": [],
    "santral_boundary": None,
    "restricted_areas": None,
    "dem_file": None,
    "site_plan_pdf": None,
    "roughness_mode": "Otomatik varsayım",
    "roughness_class": "Karma arazi",
    "turbine_manufacturer": "Envision",
    "turbine_model": "EN-182-8.0",
    "hub_height": 100.0,
    "wind_map_preserve_mean": True,
    "turbine_count": 10,
    "turbine_placement_mode": "Otomatik yerleşim",
    "manual_turbine_coordinates": "",
    "manual_turbine_points": [],
    "manual_turbine_excel_name": "",
    "manual_turbine_add_mode": False,
    "manual_turbine_selected_index": 0,
    "manual_turbine_move_step_m": 25.0,
    "manual_turbine_coord_system": "WGS84 / Enlem-Boylam",
    "manual_turbine_province": "Ankara",
    "manual_turbine_ed50_zone": 36,
    "manual_turbine_itrf_cm": 36,
    "manual_turbine_custom_epsg": 4326,
    "crosswind_spacing_d": 2.5,
    "downwind_spacing_d": 6.0,
    "dominant_wind_direction": None,
    "setback": 0.0,
    "loss_scenario": "P50",
    "wind_grid": None,
    "turbine_layout": None,
    "wake_result": None,
    "production_result": None,
    "wind_uploader_nonce": 0,
    "sensor_heights": {},
    "data_source": "LoggerNet klasörü",
    "loggernet_folder": r"C:\Campbellsci\veriler",
    "loggernet_last_scan": None,
    "loggernet_weekly_day": "Pazartesi",
    "loggernet_weekly_time": "11:00",
    "loggernet_schedule_confirmed": False,
    "loggernet_new_files": [],
    "loggernet_changed_files": [],
    "loggernet_last_data_update": None,
    "boundary_uploader_nonce": 0,
    "restricted_uploader_nonce": 0,
    "dem_uploader_nonce": 0,
    "site_plan_pdf_nonce": 0,
    "mast_installation_reports": {},
    "mast_registry": {},
    "micrositing_selected_wind_data": [],
    "installation_report_nonce": 0,
    "highres_topography_file": None,
    "highres_topography_files": [],
    "micrositing_topography_ready": False,
    "highres_topography_summary": None,
    "highres_topography_points": None,
    "highres_topography_crs": "",
    "highres_topography_scale": "1/5000",
    "highres_topography_grid_m": 5.0,
    "highres_topography_buffer_km": 5.0,
    "oda_converter_path": "",
    "wind_map_area_km": 10.0,
    "wind_map_grid_density": 60,
    "wind_map_engine": "Global Wind Atlas (GWA)",
    "gwa_wind_tif": None,
    "gwa_wind_tif_nonce": 0,
    "gwa_api_url": "",
    "gwa_height_m": 100,
    "gwa_calibrate_to_masts": True,
    "gwa_auto_download": True,
    "gwa_country_iso3": "",
    "gwa_last_source": "",
    "active_page": "Ana Sayfa",
    "measurement_step": 1,
}

# ============================================================
# SEKMEYE OZEL PROJE / OTURUM DURUMU
# ============================================================
# F5 / Ctrl+F5 ayni sekmedeki projeyi korur. localhost:8501 yeni bir
# sekmede acildiginda yeni bir oturum kimligi uretilir ve temiz proje baslar.

SEKME_STATE_KLASORU = Path.home() / ".maki_wind_studio" / "tab_sessions"
SEKME_STATE_KLASORU.mkdir(parents=True, exist_ok=True)

def _query_param_degeri(ad):
    try:
        deger = st.query_params.get(ad)
        if isinstance(deger, (list, tuple)):
            return str(deger[0]) if deger else ""
        return str(deger or "")
    except Exception:
        try:
            deger = st.experimental_get_query_params().get(ad, [""])
            return str(deger[0] if isinstance(deger, list) else deger)
        except Exception:
            return ""

def _query_param_ayarla(ad, deger):
    try:
        st.query_params[ad] = deger
    except Exception:
        try:
            mevcut = st.experimental_get_query_params()
            mevcut[ad] = deger
            st.experimental_set_query_params(**mevcut)
        except Exception:
            pass

OTURUM_SURUMU = "v1183"
_SEKME_OTURUM_ID = _query_param_degeri("msid").strip()
if not re.fullmatch(rf"{OTURUM_SURUMU}_[A-Za-z0-9_-]{{8,64}}", _SEKME_OTURUM_ID):
    _SEKME_OTURUM_ID = f"{OTURUM_SURUMU}_{uuid.uuid4().hex[:20]}"
    _query_param_ayarla("msid", _SEKME_OTURUM_ID)

SEKME_DURUM_DOSYASI = SEKME_STATE_KLASORU / f"{_SEKME_OTURUM_ID}.pkl"

_ESKI_SEKME_DOSYASI = SEKME_DURUM_DOSYASI
_BULUT_PROJE_ID = _query_param_degeri("pid").strip()
_ILK_PROJE_GECISI = not _BULUT_PROJE_ID
if _BULUT_PROJE_ID and not re.fullmatch(r"[a-f0-9]{64}", _BULUT_PROJE_ID):
    st.error("Proje bağlantısı geçersiz. Tam proje bağlantısını kullanın.")
    st.stop()
if not _BULUT_PROJE_ID:
    _BULUT_PROJE_ID = uuid.uuid4().hex + uuid.uuid4().hex
    _query_param_ayarla("pid", _BULUT_PROJE_ID)
SEKME_DURUM_DOSYASI = SEKME_STATE_KLASORU / f"{_SEKME_OTURUM_ID}_{_BULUT_PROJE_ID[:20]}.pkl"

KALICI_STATE_ANAHTARLARI = {
    "quality_flags", "quality_approvals", "cloud_project_id",
    "wind_data_files", "active_wind_data", "date_start", "date_end",
    "mast_coordinates", "selected_masts", "selected_wind_data",
    "santral_boundary", "restricted_areas", "dem_file", "site_plan_pdf",
    "roughness_mode", "roughness_class", "turbine_manufacturer",
    "turbine_model", "hub_height", "wind_map_preserve_mean",
    "turbine_count", "turbine_placement_mode", "manual_turbine_coordinates",
    "manual_turbine_points", "manual_turbine_excel_name",
    "manual_turbine_add_mode", "manual_turbine_selected_index", "manual_turbine_move_step_m",
    "manual_turbine_coord_system", "manual_turbine_province", "manual_turbine_ed50_zone",
    "manual_turbine_itrf_cm", "manual_turbine_custom_epsg",
    "crosswind_spacing_d", "downwind_spacing_d",
    "dominant_wind_direction", "setback", "loss_scenario",
    "sensor_heights", "data_source", "loggernet_folder",
    "loggernet_last_scan", "loggernet_new_files", "loggernet_changed_files",
    "loggernet_last_data_update", "mast_installation_reports",
    "mast_registry", "micrositing_selected_wind_data",
    "highres_topography_file", "highres_topography_files",
    "micrositing_topography_ready", "highres_topography_summary",
    "highres_topography_points", "highres_topography_crs",
    "highres_topography_scale", "highres_topography_grid_m",
    "highres_topography_buffer_km", "oda_converter_path",
    "wind_map_area_km", "wind_map_grid_density", "wind_map_engine",
    "gwa_wind_tif", "gwa_api_url", "gwa_height_m", "gwa_calibrate_to_masts",
    "gwa_auto_download", "gwa_country_iso3", "gwa_last_source",
    "active_page", "measurement_step",
}

def kalici_durumu_yukle():
    source = SEKME_DURUM_DOSYASI
    if not source.exists() and _ILK_PROJE_GECISI:
        source = _ESKI_SEKME_DOSYASI
    if not source.exists():
        return {}
    try:
        with source.open("rb") as dosya:
            durum = pickle.load(dosya)
        return durum if isinstance(durum, dict) else {}
    except Exception:
        try:
            SEKME_DURUM_DOSYASI.unlink(missing_ok=True)
        except Exception:
            pass
        return {}

def kalici_durumu_kaydet(durum):
    try:
        if globals().get("_BULUT_PROJE_HAZIR"):
            bulut_proje_ayarlarini_esitle(durum)
        kayit = {anahtar: durum.get(anahtar) for anahtar in KALICI_STATE_ANAHTARLARI if anahtar in durum}
        gecici = SEKME_DURUM_DOSYASI.with_suffix("." + uuid.uuid4().hex + ".tmp")
        with gecici.open("wb") as dosya:
            pickle.dump(kayit, dosya, protocol=pickle.HIGHEST_PROTOCOL)
        gecici.replace(SEKME_DURUM_DOSYASI)
        return True
    except Exception:
        return False

if "app_state" not in st.session_state:
    _kayitli_durum = kalici_durumu_yukle()
    _baslangic = APP_STATE_DEFAULTS.copy()
    _baslangic.update(_kayitli_durum)
    st.session_state.app_state = _baslangic
else:
    for _anahtar, _varsayilan in APP_STATE_DEFAULTS.items():
        st.session_state.app_state.setdefault(_anahtar, _varsayilan)

app_state = st.session_state.app_state
if app_state.get("cloud_project_id") not in (None, _BULUT_PROJE_ID):
    # A different project URL must not inherit the prior project's measurements or flags.
    st.session_state.app_state = json.loads(json.dumps(APP_STATE_DEFAULTS, default=str))
    app_state = st.session_state.app_state
    for _state_key in list(st.session_state):
        if _state_key != "app_state":
            st.session_state.pop(_state_key, None)
app_state["cloud_project_id"] = _BULUT_PROJE_ID
app_state.setdefault("quality_flags", {})
app_state.setdefault("quality_approvals", {})
for _qkey, _qvalue in app_state["quality_flags"].items():
    st.session_state.setdefault(_qkey, list(_qvalue))


# Per-project transfer store. The random URL token is a capability: never list projects.
BULUT_ORTAK_ALANLAR = ('sensor_heights', 'mast_registry', 'mast_coordinates', 'quality_flags')


@st.cache_resource(show_spinner=False)
def _bulut_proje_kilidi():
    import threading
    return threading.RLock()


def _bulut_proje_dizini():
    if not re.fullmatch(r'[a-f0-9]{64}', _BULUT_PROJE_ID):
        raise ValueError('Geçersiz proje bağlantısı.')
    return Path(__file__).resolve().parent / '.maki_runtime' / 'cloud_projects' / _BULUT_PROJE_ID


def _bulut_manifest_oku():
    path = _bulut_proje_dizini() / 'manifest.json'
    if not path.exists():
        return {'schema': 1, 'revision': None, 'files': [], 'settings': {}}
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 1 or not isinstance(manifest.get('files'), list):
        raise ValueError('Bulut proje kaydı okunamadı; son çalışma verisi korunuyor.')
    return manifest


def _bulut_manifest_yaz(manifest):
    root = _bulut_proje_dizini()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    manifest['revision'] = uuid.uuid4().hex
    temp = root / ('.manifest-' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_text(json.dumps(manifest, ensure_ascii=False, default=str), encoding='utf-8')
        os.replace(temp, root / 'manifest.json')
    finally:
        temp.unlink(missing_ok=True)


def _bulut_kayitlari(manifest):
    records = []
    for item in manifest['files']:
        digest = item.get('sha256', '')
        if not re.fullmatch(r'[a-f0-9]{64}', digest):
            raise ValueError('Bulut dosya imzası geçersiz; çalışma verisi değiştirilmedi.')
        path = _bulut_proje_dizini() / (digest + '.dat')
        if not path.is_file() or path.stat().st_size != item['size']:
            raise ValueError('Bulut aktarımı eksik; çalışma verisi değiştirilmedi.')
        records.append({**item, 'source_path': str(path), 'source': 'browser_loggernet',
                        'type': 'text/plain'})
    return records


def bulut_loggernet_yayinla(record):
    """Commit a verified whole-file snapshot atomically; preserve other masts and settings."""
    content = record.get('bytes')
    if content is None and record.get('source_path'):
        content = Path(record['source_path']).read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest != record.get('sha256') or len(content) != record['size']:
        raise ValueError('Buluta kaydetmeden önce dosya bütünlüğü kontrolü başarısız.')
    with _bulut_proje_kilidi():
        manifest = _bulut_manifest_oku()
        files = list(manifest['files'])
        if any(x['folder_id'] != record['folder_id'] for x in files):
            raise ValueError('Bu projeye başka bir klasör bağlı; farklı direk grupları karıştırılmaz.')
        names = [x['name'] for x in files]
        if record['name'] not in names and any(n.casefold() == record['name'].casefold() for n in names):
            raise ValueError('Aynı adlı dosyalar birleştirilemez.')
        metadata = {k: record[k] for k in ('name', 'sha256', 'size', 'folder_id', 'mtime_ms')}
        metadata['received_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
        if record['name'] in names:
            files[names.index(record['name'])] = metadata
        else:
            files.append(metadata)
        if sum(x['size'] for x in files) > 256 * 1024 * 1024:
            raise ValueError('Bu proje için 256 MB aktarım sınırı aşıldı; önceki veri korundu.')
        root = _bulut_proje_dizini()
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        blob = root / (digest + '.dat')
        # Rewrite even an existing same-hash cache if its bytes were damaged.
        if not blob.exists() or hashlib.sha256(blob.read_bytes()).hexdigest() != digest:
            temp = root / ('.file-' + uuid.uuid4().hex + '.tmp')
            try:
                temp.write_bytes(content)
                os.replace(temp, blob)
            finally:
                temp.unlink(missing_ok=True)
        manifest['files'] = files
        _bulut_manifest_yaz(manifest)
        # Keep retired blobs briefly so another browser can finish an in-flight read.
        current = {x['sha256'] + '.dat' for x in files}
        retired = manifest.setdefault('retired', {})
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        for previous in root.glob('*.dat'):
            if previous.name in current:
                retired.pop(previous.name, None)
            else:
                retired.setdefault(previous.name, now)
                if now - retired[previous.name] > 600:
                    try:
                        previous.unlink()
                        retired.pop(previous.name, None)
                    except OSError:
                        pass
        if retired or 'retired' in manifest:
            # Atomic rewrite retains the already chosen revision and file ordering.
            temp = root / ('.manifest-' + uuid.uuid4().hex + '.tmp')
            try:
                temp.write_text(json.dumps(manifest, ensure_ascii=False, default=str), encoding='utf-8')
                os.replace(temp, root / 'manifest.json')
            finally:
                temp.unlink(missing_ok=True)
        return _bulut_kayitlari(manifest), manifest['revision']


def bulut_proje_ayarlarini_esitle(durum):
    """Merge only changed fields, retaining unrelated browser navigation/preferences."""
    if durum.get('data_source') == 'Manuel dosya yükleme':
        return None
    baseline = st.session_state.get('_bulut_ayar_baslangici')
    local = json.loads(json.dumps({k: durum.get(k, {}) for k in BULUT_ORTAK_ALANLAR}, default=str))
    with _bulut_proje_kilidi():
        manifest = _bulut_manifest_oku()
        remote = manifest.setdefault('settings', {})
        changed = False
        for key in BULUT_ORTAK_ALANLAR:
            if baseline is None:
                if key in remote:
                    durum[key] = remote[key]
                elif local[key]:
                    remote[key] = local[key]
                    changed = True
            else:
                base = baseline.get(key, {})
                other = remote.get(key, {})
                if local[key] != base and other == base:
                    remote[key] = local[key]
                    changed = True
                elif other != base:
                    if local[key] != base and local[key] != other:
                        st.session_state['_bulut_ayar_uyarisi'] = 'Eşzamanlı değişen proje ayarı için buluttaki son kayıt alındı; düzenlemeyi kontrol edin.'
                    durum[key] = other
        if changed:
            _bulut_manifest_yaz(manifest)
        st.session_state['_bulut_ayar_baslangici'] = json.loads(json.dumps(
            {k: durum.get(k, {}) for k in BULUT_ORTAK_ALANLAR}, default=str))
        return manifest['revision']


def bulut_proje_verisini_al():
    """Load shared measurements once per revision, without requesting a local folder."""
    # Migrate an already connected browser session, never a manual project or other folder.
    with _bulut_proje_kilidi():
        manifest = _bulut_manifest_oku()
    if app_state.get('data_source') == 'Manuel dosya yükleme':
        st.session_state['_bulut_ayar_baslangici'] = None
        st.session_state.pop('_bulut_dosya_imzalari', None)
        st.session_state['_bulut_manifest_surumu'] = manifest['revision']
        return
    existing = app_state.get('wind_data_files', [])
    if not manifest['files'] and existing and all(x.get('source') == 'browser_loggernet' for x in existing):
        for record in existing:
            bulut_loggernet_yayinla(record)
    old_heights = json.dumps(app_state.get('sensor_heights', {}), sort_keys=True, default=str)
    bulut_proje_ayarlarini_esitle(app_state)
    if old_heights != json.dumps(app_state.get('sensor_heights', {}), sort_keys=True, default=str):
        for key in list(st.session_state):
            if str(key).startswith('sensor_height::'):
                st.session_state.pop(key, None)
    with _bulut_proje_kilidi():
        manifest = _bulut_manifest_oku()
        if app_state.get('data_source') != 'Manuel dosya yükleme' and manifest['files']:
            if st.session_state.get('_bulut_dosya_imzalari') != [(x['name'], x['sha256']) for x in manifest['files']]:
                records = _bulut_kayitlari(manifest)
                for record in records:
                    with open(record['source_path'], 'rb') as file:
                        if hashlib.file_digest(file, 'sha256').hexdigest() != record['sha256']:
                            raise ValueError('Buluttaki dosya bütünlüğü doğrulanamadı; önceki veri korunuyor.')
                app_state['wind_data_files'] = records
                app_state['data_source'] = 'Tarayıcı LoggerNet klasörü'
                app_state['loggernet_last_data_update'] = datetime.datetime.fromtimestamp(
                    max(x['mtime_ms'] for x in records) / 1000).isoformat(timespec='seconds')
                st.session_state['_bulut_dosya_imzalari'] = [(x['name'], x['sha256']) for x in manifest['files']]
                for key in ('wind_grid', 'wake_result', 'production_result'):
                    app_state[key] = None
        # Synchronize manual flags before the normal code computes clean measurements.
        flags = app_state.get('quality_flags', {})
        for key in list(st.session_state):
            if str(key).startswith('qc_flags_') and key not in flags:
                st.session_state.pop(key, None)
        for key, value in flags.items():
            if str(key).startswith('qc_flags_'):
                st.session_state[key] = list(value)
        st.session_state['_bulut_manifest_surumu'] = manifest['revision']
        st.session_state['_bulut_manifest_ozeti'] = {
            'count': len(manifest['files']),
            'received_at': max((x.get('received_at', '') for x in manifest['files']), default='')}


@st.fragment(run_every=10)
def bulut_proje_canli_durumu():
    try:
        with _bulut_proje_kilidi():
            manifest = _bulut_manifest_oku()
        if manifest['revision'] != st.session_state.get('_bulut_manifest_surumu'):
            st.rerun(scope='app')
        if app_state.get('data_source') == 'Manuel dosya yükleme':
            st.caption('Bu sekmede manuel veri seti kullanılıyor; ortak LoggerNet verisi bunun üzerine yazılmaz. Ortak proje bağlantısını yeni sekmede açarak LoggerNet verisine dönebilirsiniz.')
        elif manifest['files']:
            st.caption(f"Ortak projede {len(manifest['files'])} LoggerNet dosyası var. Bu panel buluttaki son veriyi kullanır; klasör izni istemez. Yeni yerel ölçümler için izin verdiğiniz Chrome sekmesi açık kalmalıdır.")
        else:
            st.info('Bu projeye henüz veri aktarılmadı. Chrome’da klasörü bağlayın; ardından Proje bağlantısını kopyala düğmesindeki adresi bu panelde açın. Bu eşleştirme bir kez yapılır.')
    except Exception as error:
        st.warning('Bulut proje kontrolü yapılamadı; son çalışma verisi korunuyor. ' + str(error))


def dosyayi_kaydet(uploaded_file):
    if uploaded_file is None:
        return None
    data = uploaded_file.getvalue()
    return {
        "name": uploaded_file.name,
        "bytes": data,
        "type": getattr(uploaded_file, "type", None),
        "size": len(data),
    }


def yukleme_listesi_degisti(uploaded_files, kayitli_dosyalar):
    """Aynı uploader dosyalarını her rerun'da tekrar onlarca MB kopyalamayı önler."""
    yeni = [(f.name, int(getattr(f, "size", 0))) for f in (uploaded_files or [])]
    eski = [(d.get("name"), int(d.get("size", 0))) for d in (kayitli_dosyalar or [])]
    return yeni != eski


def tek_yukleme_degisti(uploaded_file, kayit):
    if uploaded_file is None:
        return False
    if not kayit:
        return True
    return (uploaded_file.name, int(getattr(uploaded_file, "size", 0))) != (
        kayit.get("name"), int(kayit.get("size", 0))
    )


def kayitli_dosyayi_olustur(kayit):
    if not kayit:
        return None
    if kayit.get("source_path"):
        return KayitliDosya(
            kayit["name"],
            mime_type=kayit.get("type"),
            source_path=kayit["source_path"],
            size=kayit.get("size", 0),
        )
    return KayitliDosya(kayit["name"], kayit.get("bytes", b""), kayit.get("type"))


def loggernet_winddata_dosyalarini_bul(klasor):
    """LoggerNet klasöründeki WindData .dat dosyalarını bulur; RawData dosyalarını dışlar."""
    yol = Path(str(klasor)).expanduser()
    if not yol.exists() or not yol.is_dir():
        return []
    dosyalar = []
    for dosya in yol.iterdir():
        ad_kucuk = dosya.name.lower()
        if dosya.is_file() and ad_kucuk.endswith("winddata.dat") and "rawdata" not in ad_kucuk:
            stat = dosya.stat()
            dosyalar.append({
                "name": dosya.name,
                "source_path": str(dosya.resolve()),
                "type": "text/plain",
                "size": int(stat.st_size),
                "mtime_ns": int(stat.st_mtime_ns),
                "source": "loggernet",
            })
    return sorted(dosyalar, key=lambda x: x["name"].lower())


def loggernet_kayitlari_degisti(yeni, eski):
    yeni_imza = [(x.get("source_path"), x.get("size"), x.get("mtime_ns")) for x in yeni]
    eski_loggernet = [x for x in (eski or []) if x.get("source") == "loggernet"]
    eski_imza = [(x.get("source_path"), x.get("size"), x.get("mtime_ns")) for x in eski_loggernet]
    return yeni_imza != eski_imza


def loggernet_otomatik_senkronize(klasor, mevcut_kayitlar):
    """LoggerNet WindData dosyalarını tarar ve değişiklik özetini döndürür.

    Fonksiyon yalnızca dosya metadatasını okur; büyük .dat dosyalarını bu aşamada
    belleğe almaz. Böylece her Streamlit yeniden çalışmasında hızlı kalır.
    """
    bulunan = loggernet_winddata_dosyalarini_bul(klasor)
    eski_loggernet = {
        x.get("source_path"): x
        for x in (mevcut_kayitlar or [])
        if x.get("source") == "loggernet" and x.get("source_path")
    }
    yeni_map = {x.get("source_path"): x for x in bulunan}

    yeni_dosyalar = [
        x["name"] for yol, x in yeni_map.items() if yol not in eski_loggernet
    ]
    degisen_dosyalar = [
        x["name"]
        for yol, x in yeni_map.items()
        if yol in eski_loggernet
        and (
            x.get("size") != eski_loggernet[yol].get("size")
            or x.get("mtime_ns") != eski_loggernet[yol].get("mtime_ns")
        )
    ]
    silinen_dosyalar = [
        x.get("name") for yol, x in eski_loggernet.items() if yol not in yeni_map
    ]

    son_guncelleme = None
    if bulunan:
        son_ns = max(int(x.get("mtime_ns", 0)) for x in bulunan)
        son_guncelleme = datetime.datetime.fromtimestamp(son_ns / 1_000_000_000)

    return {
        "files": bulunan,
        "changed": loggernet_kayitlari_degisti(bulunan, mevcut_kayitlar),
        "new_files": yeni_dosyalar,
        "changed_files": degisen_dosyalar,
        "removed_files": silinen_dosyalar,
        "last_data_update": son_guncelleme,
    }


# Browser directory access is read-only; no local path is opened on the cloud host.
LOGGERNET_TARAYICI_HTML = r'''<!doctype html><html lang="tr"><meta charset="utf-8">
<style>body{font:13px 'Segoe UI',sans-serif;margin:6px;color:#17366f;background:#f5f9fc;border-radius:10px;padding:10px}button{border:1px solid #8bc53f;border-radius:8px;padding:9px;margin:3px 0;background:#fff;color:#17366f;cursor:pointer}#status{white-space:pre-wrap;overflow-wrap:anywhere;margin-top:8px}small{display:block;margin-top:6px}button:disabled{opacity:.5;cursor:default}</style>
<strong>LoggerNet · Ortak proje bağlantısı</strong><br>
<label for="projectLink">Aynı verileri diğer tarayıcıda aç:</label>
<input id="projectLink" readonly style="box-sizing:border-box;width:100%;padding:7px;margin:5px 0;border:1px solid #b6c9d7;border-radius:6px" aria-label="Ortak proje bağlantısı">
<button id="copyProject">Proje bağlantısını kopyala</button>
<small>Bu bağlantı proje verilerine erişim sağlar; yalnızca kendi tarayıcınızla veya yetkili kişilerle paylaşın.</small><br>
<button id="connect">Klasörü bağla / izni yenile</button>
<button id="scan">Şimdi tara</button><button id="stop">Takibi durdur</button>
<div id="status">Klasör izni bekleniyor.</div>
<small>Yalnızca seçili klasördeki WindData.dat dosyaları okunur. Dosyalar analiz için bu bulut uygulamasına gönderilir. Sekme açık kalmalıdır.</small>
<script>
let args={},handle=null,folderId=null,running=false,busy=false,pending=null,waiting=null,revision=new Map(),timer=null,db=null,initialized=false;
const status=document.getElementById('status');
function show(text){status.textContent=text;parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',height:Math.max(230,document.body.scrollHeight+16)},'*')}
function emit(value){parent.postMessage({isStreamlitMessage:true,type:'streamlit:setComponentValue',value,dataType:'json'},'*')}
async function database(){if(db)return db;db=await new Promise((yes,no)=>{let r=indexedDB.open('maki_loggernet_readonly_v1',1);r.onupgradeneeded=()=>r.result.createObjectStore('folders');r.onsuccess=()=>yes(r.result);r.onerror=()=>no(r.error)});return db}
async function store(value){const d=await database();await new Promise((yes,no)=>{let tx=d.transaction('folders','readwrite');tx.objectStore('folders').put(value,args.session_id);tx.oncomplete=yes;tx.onerror=()=>no(tx.error)})}
async function load(key=args.session_id){const d=await database();return await new Promise((yes,no)=>{let r=d.transaction('folders').objectStore('folders').get(key);r.onsuccess=()=>yes(r.result);r.onerror=()=>no(r.error)})}
const matches=name=>name.toLowerCase().endsWith('winddata.dat')&&!name.toLowerCase().includes('rawdata');
function schedule(){clearTimeout(timer);if(running)timer=setTimeout(scan,15000)}
async function transmit(value){const id=crypto.randomUUID();value.event_id=id;pending={id};emit(value);await new Promise((resolve,reject)=>{waiting={resolve,reject};pending.timeout=setTimeout(()=>{pending=null;waiting=null;reject(new Error('Sunucudan aktarım teyidi gelmedi. Sonraki taramada yeniden denenecek.'))},90000)})}
async function scan(){
 if(!running||busy||!handle)return;
 if(!args.enabled){show('Takip duraklatıldı: manuel veri seçili.');schedule();return}
 busy=true;
 try{
  if(await handle.queryPermission({mode:'read'})!=='granted'){running=false;show('Klasör izni gerekli. Klasörü bağla düğmesine basın.');return}
  const entries=[];for await(const [name,h] of handle.entries())if(h.kind==='file'&&matches(name))entries.push([name,h]);
  entries.sort((a,b)=>a[0].localeCompare(b[0]));
  let count=0;const warnings=[];
  for(const [name,h] of entries){
   if(!running)break;
   const file=await h.getFile(),stamp=`${file.size}:${file.lastModified}`;
   if(revision.get(name)===stamp&&args.known?.[name])continue;
   if(file.size>64*1024*1024){warnings.push(`${name}: 64 MB aktarım sınırını aşıyor; önceki veri korunuyor.`);continue}
   // LoggerNet may be writing. Recheck metadata and require a complete final line.
   const bytes=new Uint8Array(await file.arrayBuffer()),after=await h.getFile();
   if(after.size!==file.size||after.lastModified!==file.lastModified||!bytes.length||bytes[bytes.length-1]!==10){warnings.push(`${name}: yazım sürüyor veya son satır tamamlanmamış; sonraki tarama beklenecek.`);continue}
   const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');
   if(args.known?.[name]===digest){revision.set(name,stamp);continue}
   const partSize=4*1024*1024,parts=Math.ceil(bytes.length/partSize),transferId=crypto.randomUUID();
   for(let part=0;part<parts;part++){
    const slice=bytes.subarray(part*partSize,Math.min(bytes.length,(part+1)*partSize));
    let binary='';for(let i=0;i<slice.length;i+=32768)binary+=String.fromCharCode(...slice.subarray(i,i+32768));
    show(`${name} buluta aktarılıyor… ${part+1}/${parts}`);
    await transmit({action:'chunk',transfer_id:transferId,part_index:part,parts,folder_id:folderId,folder_name:handle.name,name,mtime_ms:file.lastModified,size:file.size,sha256:digest,base64:btoa(binary)});
   }
   revision.set(name,stamp);count++;
  }
  if(running){
   const available=new Set(entries.map(x=>x[0]));const missing=Object.keys(args.known||{}).filter(x=>!available.has(x));
   show(`${handle.name}: ${entries.length} dosya; ${count} güncelleme. Son tarama: ${new Date().toLocaleTimeString('tr-TR')}.`+(missing.length?'\nKlasörde artık bulunmayan kayıtlar korunuyor: '+missing.join(', '):'')+(warnings.length?'\n'+warnings.join('\n'):'')+'\n15 saniyede bir kontrol edilir.');
  }
 }catch(e){show('Aktarım yapılamadı; önceki veri korunuyor. '+e.message)}finally{busy=false;schedule()}
}
document.getElementById('copyProject').onclick=async()=>{
 const box=document.getElementById('projectLink');
 try{await navigator.clipboard.writeText(box.value);show('Proje bağlantısı kopyalandı. Aynı verileri görmek için bu adresi diğer tarayıcının adres çubuğuna yapıştırın.')}catch(_){box.focus();box.select();show('Bağlantı kutusu seçildi. Kopyalayıp diğer tarayıcının adres çubuğuna yapıştırın.')}
};
document.getElementById('connect').onclick=async()=>{
 try{
  if(!('showDirectoryPicker'in window)||!isSecureContext){show('Bu tarayıcı klasör iznini desteklemiyor. Uygulamayı güncel Chrome veya Edge içinde açın.');return}
  if(!args.enabled){show('Manuel veri yerine klasör takibini kullanmak için uygulamadaki “Tarayıcı klasör takibine dön” düğmesine basın.');return}
  // Picker must run directly from a user gesture; never request write permission.
  const chosen=await window.showDirectoryPicker({mode:'read',id:'maki-loggernet-readonly'});
  let same=handle&&await handle.isSameEntry(chosen);
  if(handle&&!same&&Object.keys(args.known||{}).length){show('Direkleri karıştırmamak için farklı klasörü yeni bir proje sekmesinde bağlayın.');return}
  handle=chosen;if(!same||!folderId){folderId=crypto.randomUUID();revision.clear()}
  try{await store({handle,folderId,paused:false})}catch(_){}
  running=true;show('Klasör bağlandı; dosyalar taranıyor.');scan();
 }catch(e){show(e.name==='AbortError'?'Bu tarayıcıda klasör seçimi veya izin işlemi tamamlanamadı. Chrome’dan aynı proje bağlantısına alınan veriler burada izin istenmeden kullanılabilir.':'Klasör izni alınamadı: '+e.message)}
};
document.getElementById('scan').onclick=()=>{if(!running){show('Önce Klasörü bağla düğmesiyle okuma izni verin.');return}scan()};
document.getElementById('stop').onclick=()=>{running=false;clearTimeout(timer);store({handle,folderId,paused:true}).catch(()=>{});show('Otomatik takip durduruldu. Son alınan ölçümler korunuyor.')};
window.addEventListener('message',async e=>{
 if(e.source!==parent||e.data?.type!=='streamlit:render')return;
 args=e.data.args||{};
 if(args.project_id){const url=new URL('/',location.origin);url.searchParams.set('pid',args.project_id);document.getElementById('projectLink').value=url.href}
 if(!handle&&args.has_remote_files)show('Bu projedeki dosyalar buluttan hazır. Bu panelde klasör izni gerekmez. Yeni yerel veriler için izin verdiğiniz Chrome sekmesi açık kalmalıdır.');
 if(pending&&args.ack?.id===pending.id){clearTimeout(pending.timeout);const wait=waiting;pending=null;waiting=null;if(args.ack.ok)wait.resolve();else wait.reject(new Error(args.ack.message||'Dosya reddedildi.'))}
 if(!initialized){initialized=true;try{const saved=(await load())||(args.legacy_session_id?await load(args.legacy_session_id):null);if(saved){try{await store(saved)}catch(_){}handle=saved.handle;folderId=saved.folderId;if(saved.paused){show('Takip durdurulmuş. Klasörü bağla düğmesiyle yeniden başlatın.')}else if(await handle.queryPermission({mode:'read'})==='granted'){running=true;scan()}else show('Kayıtlı klasör için izni yenileyin.')}}catch(_){} }
});
window.addEventListener('beforeunload',()=>{running=false;clearTimeout(timer)});
parent.postMessage({isStreamlitMessage:true,type:'streamlit:componentReady',apiVersion:1},'*');
show('Klasörü bağla düğmesine basıp C:\\Campbellsci\\veriler klasörünü seçin.');
</script></html>'''


def tarayici_loggernet_kaydini_hazirla(event, _content=None):
    """Validate one complete read-only snapshot before replacing any application data."""
    if not isinstance(event, dict) or event.get('action') != 'file':
        raise ValueError('Geçersiz aktarım mesajı.')
    name = event.get('name', '')
    if not isinstance(name, str) or not name or any(x in name for x in ('/', '\\', '\x00')):
        raise ValueError('Geçersiz dosya adı.')
    if not name.lower().endswith('winddata.dat') or 'rawdata' in name.lower():
        raise ValueError('Yalnızca WindData.dat dosyaları kabul edilir.')
    size = event.get('size')
    if not isinstance(size, int) or isinstance(size, bool) or not 0 < size <= 64 * 1024 * 1024:
        raise ValueError('Dosya boyutu 0–64 MB aralığında olmalıdır.')
    if _content is None:
        encoded = event.get('base64')
        if not isinstance(encoded, str) or len(encoded) > 4 * ((size + 2) // 3):
            raise ValueError('Aktarım boyutu uyuşmuyor.')
        try:
            content = base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError):
            raise ValueError('Dosya aktarımı çözülemedi.') from None
    else:
        # Only the server-side chunk assembler supplies bytes here. No JSON field
        # skips the size/hash/parser checks below.
        if not isinstance(_content, bytes):
            raise ValueError('Geçersiz aktarım içeriği.')
        content = _content
    if len(content) != size or hashlib.sha256(content).hexdigest() != event.get('sha256'):
        raise ValueError('Dosya bütünlüğü doğrulanamadı; önceki veri korunuyor.')
    if not content.endswith(b'\n'):
        raise ValueError('Son satır tamamlanmamış; sonraki tarama beklenecek.')
    folder_id = event.get('folder_id', '')
    if not isinstance(folder_id, str) or not re.fullmatch(r'[a-f0-9-]{36}', folder_id):
        raise ValueError('Geçersiz klasör kimliği.')
    mtime = event.get('mtime_ms')
    if not isinstance(mtime, (int, float)) or isinstance(mtime, bool) or not np.isfinite(mtime) or mtime < 0:
        raise ValueError('Geçersiz dosya güncelleme zamanı.')
    parsed = getattr(loggernet_oku, '__wrapped__', loggernet_oku)(content)
    if parsed.empty or parsed.attrs.get('discarded_invalid_times', 0):
        raise ValueError('Dosya eksik/bozuk zaman kayıtları içeriyor; önceki veri korunuyor.')
    return {'name': name, 'bytes': content, 'type': 'text/plain', 'size': size,
            'source': 'browser_loggernet', 'folder_id': folder_id,
            'sha256': event['sha256'], 'mtime_ms': float(mtime)}


def tarayici_loggernet_kaydini_uygula(event, _content=None):
    """Reject mixed sources/folders and preserve order, so existing mast keys remain stable."""
    record = tarayici_loggernet_kaydini_hazirla(event, _content=_content)
    existing = app_state.get('wind_data_files', [])
    if any(x.get('source') != 'browser_loggernet' for x in existing):
        raise ValueError('Mevcut proje verilerini korumak için klasörü boş bir proje sekmesinde bağlayın.')
    if any(x.get('folder_id') != record['folder_id'] for x in existing):
        raise ValueError('Farklı klasörler karıştırılmaz. Yeni klasörü yeni bir proje sekmesinde bağlayın.')
    records = list(existing)
    names = [x['name'] for x in records]
    if record['name'] not in names and any(x.casefold() == record['name'].casefold() for x in names):
        raise ValueError('Büyük/küçük harfle ayrılan aynı dosya adı var; kaynak klasörü kontrol edin.')
    if record['name'] in names:
        records[names.index(record['name'])] = record
    else:
        records.append(record)
    records, revision = bulut_loggernet_yayinla(record)
    app_state['wind_data_files'] = records
    app_state['data_source'] = 'Tarayıcı LoggerNet klasörü'
    app_state['loggernet_last_scan'] = datetime.datetime.now().isoformat(timespec='seconds')
    app_state['loggernet_last_data_update'] = datetime.datetime.fromtimestamp(
        max(x['mtime_ms'] for x in records) / 1000).isoformat(timespec='seconds')
    # Never reuse previously computed energy/map results for refreshed measurements.
    for key in ('wind_grid', 'wake_result', 'production_result'):
        app_state[key] = None
    return record


LOGGERNET_PARCA_BOYUTU = 4 * 1024 * 1024


def tarayici_loggernet_parcasini_al(event):
    """Stage bounded chunks in this session; publish only a complete verified file."""
    name = event.get('name', '')
    total, index = event.get('size'), event.get('part_index')
    count = event.get('parts')
    transfer_id = event.get('transfer_id', '')
    if (not isinstance(name, str) or not name.lower().endswith('winddata.dat')
            or 'rawdata' in name.lower() or any(c in name for c in ('/', '\\', '\x00'))
            or not isinstance(total, int) or isinstance(total, bool) or not 0 < total <= 64 * 1024 * 1024
            or not isinstance(index, int) or isinstance(index, bool)
            or not isinstance(count, int) or isinstance(count, bool)
            or count != (total + LOGGERNET_PARCA_BOYUTU - 1) // LOGGERNET_PARCA_BOYUTU
            or not 0 <= index < count or not isinstance(transfer_id, str)
            or not re.fullmatch(r'[a-f0-9-]{36}', transfer_id)):
        raise ValueError('Geçersiz dosya aktarım parçası.')
    expected = min(LOGGERNET_PARCA_BOYUTU, total - index * LOGGERNET_PARCA_BOYUTU)
    encoded = event.get('base64')
    if not isinstance(encoded, str) or len(encoded) != 4 * ((expected + 2) // 3):
        raise ValueError('Aktarım parçası boyutu uyuşmuyor.')
    try:
        data = base64.b64decode(encoded, validate=True)
    except (TypeError, ValueError):
        raise ValueError('Aktarım parçası çözülemedi.') from None
    if len(data) != expected:
        raise ValueError('Aktarım parçası eksik.')
    metadata = tuple(event.get(k) for k in ('name', 'folder_id', 'size', 'sha256', 'mtime_ms'))
    if index == 0:
        st.session_state['_browser_loggernet_transfer'] = {
            'id': transfer_id, 'metadata': metadata, 'next': 0, 'data': bytearray()}
    staged = st.session_state.get('_browser_loggernet_transfer')
    if (not staged or staged['id'] != transfer_id or staged['metadata'] != metadata
            or staged['next'] != index):
        raise ValueError('Aktarım sırası uyuşmuyor; dosya sonraki taramada yeniden denenecek.')
    staged['data'].extend(data)
    staged['next'] += 1
    if staged['next'] == count:
        try:
            content = bytes(staged.pop('data'))
            complete = {**event, 'action': 'file'}
            tarayici_loggernet_kaydini_uygula(complete, _content=content)
        finally:
            st.session_state.pop('_browser_loggernet_transfer', None)
        return True
    return False


def tarayici_loggernet_paneli():
    folder = Path(__file__).resolve().parent / '.maki_runtime' / 'browser_loggernet_v1'
    folder.mkdir(parents=True, exist_ok=True)
    html = folder / 'index.html'
    if not html.exists() or html.read_text(encoding='utf-8') != LOGGERNET_TARAYICI_HTML:
        html.write_text(LOGGERNET_TARAYICI_HTML, encoding='utf-8')
    component = components.declare_component('maki_browser_loggernet_v1', path=str(folder))
    known = {x['name']: x.get('sha256') for x in app_state.get('wind_data_files', [])
             if x.get('source') == 'browser_loggernet'}
    if st.session_state.get('_bulut_hata'):
        known = {}  # Ask the source browser to repair a missing/rebuilt server snapshot.
    event = component(session_id='project_' + _BULUT_PROJE_ID, project_id=_BULUT_PROJE_ID,
        legacy_session_id=_SEKME_OTURUM_ID, has_remote_files=bool(known),
        enabled=app_state.get('data_source') != 'Manuel dosya yükleme', known=known,
        ack=st.session_state.get('_browser_loggernet_ack'), default=None,
        key='browser_loggernet_readonly_v1')
    if isinstance(event, dict) and event.get('event_id') != st.session_state.get('_browser_loggernet_ack', {}).get('id'):
        event_id = event.get('event_id')
        if not isinstance(event_id, str) or not re.fullmatch(r'[a-f0-9-]{36}', event_id):
            st.error('Geçersiz aktarım kimliği.')
            return
        try:
            if event.get('action') == 'chunk':
                tarayici_loggernet_parcasini_al(event)
            else:
                tarayici_loggernet_kaydini_uygula(event)
            st.session_state['_browser_loggernet_ack'] = {'id': event_id, 'ok': True}
            st.session_state.pop('_browser_loggernet_error', None)
        except Exception as error:
            st.session_state['_browser_loggernet_error'] = str(error)
            st.session_state['_browser_loggernet_ack'] = {'id': event_id, 'ok': False,
                'message': str(error)}
        st.rerun()
    if st.session_state.get('_browser_loggernet_error'):
        st.error(st.session_state['_browser_loggernet_error'])


def loggernet_programini_bul():
    """Bilinen Campbell Scientific kurulum yollarında LoggerNet Toolbar/Setup uygulamasını arar."""
    adaylar = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Campbellsci" / "LoggerNet" / "LoggerNet.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Campbellsci" / "LoggerNet" / "LoggerNet.exe",
        Path(r"C:\Campbellsci\LoggerNet\LoggerNet.exe"),
        Path(r"C:\Program Files (x86)\Campbellsci\LoggerNet\Toolbar.exe"),
        Path(r"C:\Program Files\Campbellsci\LoggerNet\Toolbar.exe"),
    ]
    for aday in adaylar:
        if aday.exists():
            return aday
    # Kurulum adları sürüme göre değişebildiğinden CampbellSci klasörlerinde sınırlı arama.
    kokler = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Campbellsci",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Campbellsci",
        Path(r"C:\Campbellsci"),
    ]
    for kok in kokler:
        if not kok.exists():
            continue
        for desen in ("*LoggerNet*.exe", "Toolbar.exe", "Setup.exe"):
            for aday in kok.rglob(desen):
                if aday.is_file():
                    return aday
    return None


def loggernet_programini_ac():
    program = loggernet_programini_bul()
    if program is None:
        return False, "LoggerNet çalıştırılabilir dosyası otomatik bulunamadı."
    try:
        subprocess.Popen([str(program)], shell=False)
        return True, str(program)
    except Exception as hata:
        return False, str(hata)


def sonraki_pazartesi_1100(simdi=None):
    simdi = simdi or datetime.datetime.now()
    hedef = simdi.replace(hour=11, minute=0, second=0, microsecond=0)
    gun_farki = (0 - simdi.weekday()) % 7
    hedef = hedef + datetime.timedelta(days=gun_farki)
    if hedef <= simdi:
        hedef += datetime.timedelta(days=7)
    return hedef


# ============================================================
# KURUMSAL ARAYÜZ / DEMO TASARIMI
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #f4f7fb;
        --surface: #ffffff;
        --line: #dce5ef;
        --text: #15366f;
        --muted: #6c7d91;
        --green: #8bc53f;
        --green-dark: #5f9829;
        --green-soft: #f1f8e8;
        --blue: #153f91;
        --blue-dark: #0c2c6a;
        --teal: #20aaa2;
        --orange: #f4a321;
        --shadow: 0 8px 24px rgba(21, 63, 145, 0.08);
        --radius: 16px;
    }
    html, body, [class*="css"] {font-family: Inter, "Segoe UI", Arial, sans-serif;}
    .stApp {
        background: radial-gradient(circle at 100% 0%, rgba(32,170,162,.11), transparent 26%), radial-gradient(circle at 0% 100%, rgba(139,197,63,.08), transparent 28%), linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
        color: var(--text);
    }
    .block-container {max-width: 1520px; padding-top: 1.15rem; padding-bottom: 3rem;}
    section[data-testid="stSidebar"] {background: linear-gradient(180deg, #0d2f72 0%, #123f89 58%, #126a7a 100%); border-right: 1px solid rgba(255,255,255,.08);}
    section[data-testid="stSidebar"] * {color: #eef9f4;}
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stDateInput label,
    section[data-testid="stSidebar"] .stFileUploader label {font-weight: 600;}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {background: rgba(255,255,255,.08); border: 1px dashed rgba(255,255,255,.28); border-radius: 14px;}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {padding: .52rem .65rem; margin-bottom: .25rem; border-radius: 10px; transition: .2s ease;}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {background: rgba(255,255,255,.08);}

    /* Sidebar form controls: light surface + dark readable text */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        background: #ffffff !important;
        color: #17352d !important;
        -webkit-text-fill-color: #17352d !important;
        caret-color: #17352d !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #17352d !important;
        border-color: #cfdad5 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] input,
    section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
        color: #17352d !important;
        -webkit-text-fill-color: #17352d !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] svg,
    section[data-testid="stSidebar"] [data-testid="stDateInput"] svg {
        fill: #355b4f !important;
        color: #355b4f !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: #f8fbf9 !important;
        border: 1px dashed #8fb3a4 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] *,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] *,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFileName"] {
        color: #17352d !important;
        -webkit-text-fill-color: #17352d !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
        background: #ffffff !important;
        border: 1px solid #d7e2dd !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"] {
        background: #ffffff !important;
        color: #17352d !important;
        border-color: #cfdad5 !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"] * {
        color: #17352d !important;
    }

    section[data-testid="stSidebar"] input::placeholder {
        color: #81938b !important;
        -webkit-text-fill-color: #81938b !important;
        opacity: 1 !important;
    }
    .app-hero {
        background: linear-gradient(110deg, #123f88 0%, #258fa3 68%, #83bd4e 100%);
        border-radius: 14px; padding: 14px 18px; margin-bottom: 12px;
        box-shadow: 0 8px 20px rgba(21, 63, 145, .13); color: white; position: relative; overflow: hidden;
    }
    .app-hero:after {content:""; position:absolute; width:110px; height:110px; right:-30px; top:-42px; border-radius:50%; border:1px solid rgba(255,255,255,.16);}
    .hero-kicker {font-size:.60rem; letter-spacing:.13em; font-weight:750; opacity:.76; text-transform:uppercase; margin-bottom:4px;}
    .hero-title {font-size:1.38rem; line-height:1.12; font-weight:800; margin:0 0 4px 0;}
    .hero-sub {font-size:.82rem; opacity:.86; max-width:900px; margin:0; line-height:1.35;}
    .hero-badges {display:flex; flex-wrap:wrap; gap:5px; margin-top:9px;}
    .hero-badge {display:inline-flex; align-items:center; gap:4px; border:1px solid rgba(255,255,255,.20); background:rgba(255,255,255,.08); padding:4px 7px; border-radius:999px; font-size:.66rem; font-weight:650;}
    .section-head {display:flex; align-items:center; justify-content:space-between; gap:12px; margin:1.2rem 0 .8rem;}
    .section-head h2 {font-size:1.18rem; margin:0; color:var(--text);}
    .section-head p {margin:.25rem 0 0; color:var(--muted); font-size:.86rem;}
    div[data-testid="stMetric"] {background:rgba(255,255,255,.92); border:1px solid var(--line); border-radius:var(--radius); padding:17px 18px; box-shadow:var(--shadow); min-height:116px;}
    div[data-testid="stMetric"] label {color:var(--muted)!important; font-weight:650!important; font-size:.79rem!important;}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {color:var(--text); font-weight:780;}
    div[data-testid="stExpander"] {background:rgba(255,255,255,.95); border:1px solid var(--line); border-radius:var(--radius); box-shadow:0 5px 18px rgba(19,50,41,.045); overflow:hidden;}
    div[data-testid="stTabs"] button {border-radius:10px 10px 0 0; padding:.72rem 1rem; font-weight:700;}
    div[data-testid="stTabs"] button[aria-selected="true"] {color:var(--green-dark); border-bottom-color:var(--green); background:var(--green-soft);}
    div[data-baseweb="select"] > div, .stNumberInput input, .stTextInput input, .stDateInput input {border-radius:11px!important; border-color:var(--line)!important;}
    [data-testid="stFileUploaderDropzone"] {border-radius:14px; border:1px dashed #aac7b9; background:#fbfdfb;}
    .stButton > button, .stDownloadButton > button {border-radius:11px; border:1px solid var(--green); font-weight:700; transition:all .18s ease;}
    .stButton > button:hover, .stDownloadButton > button:hover {transform:translateY(-1px); box-shadow:0 8px 18px rgba(15,159,104,.16);}
    div[data-testid="stAlert"] {border-radius:13px; border:1px solid rgba(15,159,104,.12);}
    div[data-testid="stDataFrame"], div[data-testid="stPlotlyChart"], div[data-testid="stVegaLiteChart"] {background:rgba(255,255,255,.96); border:1px solid var(--line); border-radius:var(--radius); padding:8px; box-shadow:0 5px 18px rgba(19,50,41,.045);}
    hr {border-color:var(--line); margin:1.5rem 0;}
    #MainMenu {visibility:hidden;} footer {visibility:hidden;} header[data-testid="stHeader"] {background:transparent;}
    .sidebar-brand {padding:8px 4px 16px; border-bottom:1px solid rgba(255,255,255,.15); margin-bottom:12px;}
    .sidebar-logo-wrap {background:#ffffff;border-radius:14px;padding:10px 12px;box-shadow:0 10px 26px rgba(4,24,70,.22);margin-bottom:11px;}
    .sidebar-logo {display:block;width:100%;max-width:205px;height:auto;margin:0 auto;}
    .sidebar-brand .sub {display:block; margin-top:8px; color:rgba(255,255,255,.76); font-size:.73rem; letter-spacing:.05em;font-weight:700;}
    .hero-logo {width:118px;max-width:30%;background:#fff;border-radius:9px;padding:5px 8px;margin-bottom:7px;box-shadow:0 5px 12px rgba(2,25,72,.12);}
    .hero-accent {position:absolute;left:0;bottom:0;width:100%;height:5px;background:linear-gradient(90deg,var(--orange),var(--green),var(--teal),#ffffff66);}
    .stButton > button[kind="primary"] {background:linear-gradient(90deg,var(--green),#a7cf55)!important;color:#12366f!important;border:1px solid #75aa2f!important;box-shadow:0 8px 20px rgba(139,197,63,.22)!important;}
    .stButton > button[kind="primary"] * {color:#12366f!important;}
    .stButton > button[kind="primary"]:hover {background:linear-gradient(90deg,var(--orange),#ffc45a)!important;border-color:#e49314!important;box-shadow:0 10px 22px rgba(244,163,33,.25)!important;}
    div[data-testid="stTabs"] button[aria-selected="true"] {color:var(--blue)!important;border-bottom-color:var(--green)!important;background:linear-gradient(180deg,#fff,var(--green-soft))!important;}
    .empty-state {background:rgba(255,255,255,.95); border:1px dashed #b7c9c0; border-radius:18px; padding:40px 28px; text-align:center; box-shadow:var(--shadow);}
    .empty-state h3 {margin:0 0 8px; color:var(--text);}
    .empty-state p {color:var(--muted); margin:0;}

    /* Sidebar menüsü: Streamlit blok yüksekliğini bozmadan kompakt ve güvenli düzen. */
    .v8-brand {
        padding-bottom: 12px !important;
        margin-bottom: 2px !important;
    }
    .v8-product-name {
        font-size: 1rem;
        font-weight: 900;
        letter-spacing: .08em;
        color: #fff;
        margin-top: 8px;
        line-height: 1.25;
    }

    /* Başlıklarda margin yerine padding kullanılır; böylece Streamlit eleman yüksekliği sıfıra düşmez. */
    .v8-menu-caption {
        display: flex !important;
        align-items: flex-end !important;
        min-height: 34px !important;
        box-sizing: border-box !important;
        padding: 14px 4px 5px 4px !important;
        margin: 0 !important;
        font-size: .66rem !important;
        font-weight: 850 !important;
        letter-spacing: .13em !important;
        line-height: 1.15 !important;
        color: rgba(255,255,255,.78) !important;
        white-space: nowrap !important;
    }

    /* Yalnızca gerçek menü düğmeleri düzenlenir. Genel vertical-block gap değerine dokunulmaz. */
    section[data-testid="stSidebar"] div[data-testid="stButton"] {
        margin: 0 0 3px 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
        min-height: 42px !important;
        height: auto !important;
        justify-content: flex-start !important;
        text-align: left !important;
        border-radius: 10px !important;
        padding: .50rem .70rem !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
        white-space: normal !important;
        border: 1px solid transparent !important;
        box-shadow: none !important;
        transition: .16s ease !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button p {
        margin: 0 !important;
        line-height: 1.25 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] {
        background:transparent!important;color:#f4f8ff!important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] * {color:#f4f8ff!important;}
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background:rgba(255,255,255,.10)!important;border-color:rgba(255,255,255,.12)!important;transform:translateX(2px)!important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
        background:linear-gradient(90deg,rgba(139,197,63,.98),rgba(32,170,162,.96))!important;
        color:#082d57!important;border-color:rgba(255,255,255,.16)!important;
        box-shadow:0 7px 16px rgba(4,28,74,.20)!important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] * {color:#082d57!important;}

    /* Streamlit/Chrome focus durumu bir menü düğmesini beyaza çevirmesin. */
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"],
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:focus,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:focus-visible,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:active {
        background: transparent !important;
        color: #f4f8ff !important;
        border-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: rgba(255,255,255,.10) !important;
        border-color: rgba(255,255,255,.12) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] *,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover *,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:focus *,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:active * {
        color: #f4f8ff !important;
        -webkit-text-fill-color: #f4f8ff !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"],
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:focus,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:focus-visible,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:active {
        background: linear-gradient(90deg,rgba(139,197,63,.98),rgba(32,170,162,.96)) !important;
        color: #082d57 !important;
        border-color: rgba(255,255,255,.16) !important;
        outline: none !important;
        box-shadow: 0 7px 16px rgba(4,28,74,.20) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] *,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:hover *,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:focus *,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:active * {
        color: #082d57 !important;
        -webkit-text-fill-color: #082d57 !important;
    }

    .v8-sub-row {margin-left:14px;position:relative;}
    .v8-sub-row:before {content:"";position:absolute;left:-9px;top:-7px;bottom:8px;width:2px;background:rgba(139,197,63,.55);border-radius:4px;}
    .v8-status-panel {margin-top:10px;padding:14px;border:1px solid rgba(255,255,255,.14);background:rgba(4,34,84,.28);border-radius:14px;}
    .v8-status-title {font-size:.66rem;letter-spacing:.13em;font-weight:850;color:rgba(255,255,255,.58);margin-bottom:10px;}
    .v8-status-item {display:flex;align-items:center;gap:8px;font-size:.82rem;color:#fff;margin-bottom:12px;}
    .v8-dot {width:9px;height:9px;border-radius:50%;display:inline-block;box-shadow:0 0 0 4px rgba(255,255,255,.06);}
    .v8-dot.ok {background:#8bc53f;}.v8-dot.wait {background:#f4a321;}
    .v8-status-grid {display:grid;grid-template-columns:1fr 1fr;gap:8px;}
    .v8-status-grid div,.v8-status-model {background:rgba(255,255,255,.07);border-radius:9px;padding:9px;}
    .v8-status-grid span,.v8-status-model span {display:block;font-size:.65rem;color:rgba(255,255,255,.62);margin-bottom:3px;}
    .v8-status-grid b,.v8-status-model b {font-size:.78rem;color:#fff;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}

    .v8-status-model {margin-top:8px;}

    /* Uzun dosya/direk adlarini uc nokta ile kesme; tam metni goster. */
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        line-height: 1.08 !important;
        font-size: clamp(1.05rem, 1.55vw, 1.85rem) !important;
    }
    div[data-baseweb="select"] > div {
        min-height: 44px !important;
        height: auto !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[aria-selected="true"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


def guvenli_dataframe(veri, *args, **kwargs):
    """PyArrow kullanmadan DataFrame benzeri veriyi gerçek HTML tablo olarak gösterir.

    Streamlit markdown ayrıştırıcısı yerine components.html kullanılır. Böylece
    HTML etiketleri ekranda metin olarak görünmez ve st.dataframe/pyarrow gerekmez.
    """
    try:
        if veri is None:
            st.info("Gösterilecek tablo verisi bulunamadı.")
            return

        if hasattr(veri, "data") and isinstance(getattr(veri, "data", None), pd.DataFrame):
            tablo = veri.data.copy()
        elif isinstance(veri, pd.DataFrame):
            tablo = veri.copy()
        elif isinstance(veri, pd.Series):
            tablo = veri.to_frame()
        else:
            tablo = pd.DataFrame(veri)

        hide_index = bool(kwargs.get("hide_index", False))
        max_satir = int(kwargs.get("max_rows", 500) or 500)
        max_satir = max(1, min(max_satir, 5000))
        toplam = len(tablo)
        gorunen = tablo.head(max_satir)

        table_html = gorunen.to_html(
            index=not hide_index,
            border=0,
            classes="maki-safe-table",
            escape=True,
            na_rep="",
        )

        satir_sayisi = max(1, min(len(gorunen), 20))
        istenen_yukseklik = kwargs.get("height")
        if istenen_yukseklik is None:
            iframe_height = min(620, 72 + satir_sayisi * 34)
        else:
            try:
                iframe_height = max(120, min(int(istenen_yukseklik), 760))
            except Exception:
                iframe_height = min(620, 72 + satir_sayisi * 34)

        belge = f"""
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <style>
            html, body {{ margin:0; padding:0; background:transparent; font-family:Inter,"Segoe UI",Arial,sans-serif; }}
            .maki-safe-table-wrap {{
                width:100%; height:{max(90, iframe_height-8)}px; overflow:auto;
                box-sizing:border-box; border:1px solid #dce5ef;
                border-radius:14px; background:#fff;
            }}
            table.maki-safe-table {{
                width:100%; border-collapse:collapse; font-size:13px; color:#15366f;
            }}
            table.maki-safe-table thead th {{
                position:sticky; top:0; z-index:2; background:#eef5fb;
                border-bottom:1px solid #cfdce9; padding:8px 10px;
                white-space:nowrap; text-align:left;
            }}
            table.maki-safe-table tbody td,
            table.maki-safe-table tbody th {{
                border-bottom:1px solid #edf1f5; padding:7px 10px;
                white-space:nowrap; text-align:left;
            }}
            table.maki-safe-table tbody tr:nth-child(even) {{ background:#f9fbfd; }}
            table.maki-safe-table tbody tr:hover {{ background:#f1f8e8; }}
        </style>
        </head>
        <body><div class="maki-safe-table-wrap">{table_html}</div></body>
        </html>
        """
        components.html(belge, height=iframe_height, scrolling=False)

        if toplam > max_satir:
            st.caption(f"Tablo performans için ilk {max_satir:,} satırla sınırlandı. Toplam: {toplam:,} satır.")
    except Exception as hata:
        st.warning(f"Tablo görüntülenemedi: {hata}")

def arayuz_hero(baslik, alt_baslik, rozetler=None):
    rozetler = rozetler or []
    badge_html = "".join(f'<span class="hero-badge">{rozet}</span>' for rozet in rozetler)
    st.markdown(
        f"""
        <div class="app-hero">
            <img class="hero-logo" src="{MAKI_LOGO_DATA_URI}" alt="Maki Enerji">
            <div class="hero-kicker">MAKİ ENERJİ · RES ANALİZ PLATFORMU</div>
            <div class="hero-title">{baslik}</div>
            <p class="hero-sub">{alt_baslik}</p>
            <div class="hero-badges">{badge_html}</div>
            <div class="hero-accent"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bolum_basligi(baslik, aciklama=""):
    st.markdown(
        f"""
        <div class="section-head">
            <div><h2>{baslik}</h2><p>{aciklama}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def suruklenebilir_lejantli_plotly(fig, height=440):
    """Plotly lejantını fareyle sürüklenebilir olarak gösterir."""
    html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config={
            "responsive": True,
            "displaylogo": False,
            "scrollZoom": False,
            "editable": True,
            "edits": {"legendPosition": True},
            "modeBarButtonsToRemove": [
                "zoom2d", "pan2d", "select2d", "lasso2d",
                "zoomIn2d", "zoomOut2d", "autoScale2d",
                "resetScale2d"
            ]
        }
    )
    components.html(html, height=height, scrolling=False)

SANTRAL = "RES Projesi"
DIREK = "Çorlu-1"

SENSORLER = {
    "83.0 m": {
        "kolon": "WS1_Avg",
        "yukseklik": 83
    },
    "78.5 m": {
        "kolon": "WS2_Avg",
        "yukseklik": 78.5
    },
    "60 m": {
        "kolon": "WS3_Avg",
        "yukseklik": 60
    },
    "40 m": {
        "kolon": "WS4_Avg",
        "yukseklik": 40
    }
}

RUZGAR_KOLONLARI = [
    "WS1_Avg",
    "WS2_Avg",
    "WS3_Avg",
    "WS4_Avg"
]

GORUNUR_ADLAR = {
    "WS1_Avg": "83.0 m",
    "WS2_Avg": "78.5 m",
    "WS3_Avg": "60.0 m",
    "WS4_Avg": "40.0 m"
}

# Evrensel başlangıç değerleri: raporda/LoggerNet başlığında bilgi yoksa 0 kullanılır.
# Hiçbir direğe ait ölçüm yüksekliği başka bir direğe varsayılan olarak taşınmaz.
VARSAYILAN_SENSOR_YUKSEKLIKLERI = {kolon: 0.0 for kolon in RUZGAR_KOLONLARI}

def sensor_etiketi(kolon, yukseklikler):
    """Grafiklerde her sensörü benzersiz ve anlaşılır adla gösterir.

    Yükseklik henüz eşleşmemişse bütün kolonları aynı ``Bulunamadı`` adına
    çevirmek Plotly grafiklerini birbirine bağlayıp bozar. Bu nedenle kolon
    adı korunur ve yalnızca yüksekliğin eksik olduğu belirtilir.
    """
    deger = float((yukseklikler or {}).get(kolon, 0.0) or 0.0)
    return f"{kolon} ({deger:g} m)" if deger > 0 else f"{kolon} (yükseklik bulunamadı)"

def sensor_yukseklik_tuple(yukseklikler):
    return tuple(float((yukseklikler or {}).get(k, 0.0) or 0.0) for k in RUZGAR_KOLONLARI)


# ============================================================

def loggernet_sensor_yuksekliklerini_algila(dosya_nesnesi):
    """TOA5 başlığı/kolon adlarında açıkça yazılmış sensör yüksekliklerini algılar.

    Örnek desteklenen kolon adları: WS1_83m_Avg, WS_78.5m, WindSpeed60m.
    Standart WS1_Avg gibi adlarda yükseklik bilgisi bulunmadığından None döner.
    """
    try:
        if getattr(dosya_nesnesi, "source_path", None):
            ham = Path(dosya_nesnesi.source_path).read_bytes()[:20000]
        else:
            ham = dosya_nesnesi.getvalue()[:20000]
        metin = ham.decode("utf-8", errors="ignore")
    except Exception:
        return {}

    bulunan = {}
    satirlar = metin.splitlines()[:8]
    baslik_metni = " ".join(satirlar)
    for kolon in RUZGAR_KOLONLARI:
        # Önce kolonun kendisi çevresinde 1-300 m aralığında bir yükseklik ara.
        desenler = [
            rf'{re.escape(kolon)}[^,;\n]{{0,20}}?(\d{{1,3}}(?:[\.,]\d+)?)\s*m\b',
            rf'{re.escape(kolon.split("_")[0])}[^,;\n]{{0,16}}?(\d{{1,3}}(?:[\.,]\d+)?)\s*m\b',
        ]
        for desen in desenler:
            eslesme = re.search(desen, baslik_metni, flags=re.IGNORECASE)
            if eslesme:
                deger = float(eslesme.group(1).replace(',', '.'))
                if 1.0 <= deger <= 300.0:
                    bulunan[kolon] = deger
                    break
    return bulunan


def vaziyet_plani_pdf_ozeti(pdf_bytes):
    """PDF'den güvenli bir ilk önizleme ve metin özeti üretir."""
    sonuc = {"sayfa_sayisi": 0, "metin": "", "onizleme_png": None, "hata": None}
    try:
        import fitz
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        sonuc["sayfa_sayisi"] = len(doc)
        metinler = []
        for sayfa in doc[: min(len(doc), 5)]:
            metinler.append(sayfa.get_text("text"))
        sonuc["metin"] = "\n".join(metinler).strip()
        if len(doc):
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            sonuc["onizleme_png"] = pix.tobytes("png")
        doc.close()
    except Exception as hata:
        sonuc["hata"] = str(hata)
    return sonuc



def _ondalik_sayi(deger):
    try:
        return float(str(deger).strip().replace(" ", "").replace(",", "."))
    except Exception:
        return None


def _dms_to_decimal(deg, minute, second, yon):
    val = float(deg) + float(minute) / 60.0 + float(second) / 3600.0
    if str(yon).upper() in {"S", "W"}:
        val *= -1
    return val


def _pdf_sayfa_ocr(sayfa):
    """Metin katmanı olmayan sayfalarda isteğe bağlı OCR uygular."""
    try:
        import io
        import pytesseract
        from PIL import Image
        pix = sayfa.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
        goruntu = Image.open(io.BytesIO(pix.tobytes("png")))
        return pytesseract.image_to_string(goruntu, lang="eng+tur")
    except Exception:
        return ""


def _pdf_tablo_metinleri(sayfa):
    """PyMuPDF tablo algılayıcısı varsa tablo hücrelerini düz metne dönüştürür."""
    satirlar = []
    try:
        tablolar = sayfa.find_tables()
        for tablo in getattr(tablolar, "tables", []):
            for satir in tablo.extract() or []:
                satirlar.append(" | ".join("" if hucre is None else str(hucre) for hucre in satir))
    except Exception:
        pass
    return "\n".join(satirlar)


def kurulum_raporu_pdf_oku(pdf_bytes):
    """Kurulum raporunun bütün sayfalarını tarar ve direk bilgilerini çıkarır.

    Okuma sırası:
    1. PDF metin katmanı
    2. Sayfadaki tablolar
    3. Metin yetersizse OCR
    4. Başlık ve bağlam tabanlı düzenli ifadeler

    Sayfa numarası kullanılmaz. Koordinat ve sensör sayfaları başlıklarından bulunur.
    """
    sonuc = {
        "sayfa_sayisi": 0,
        "metin": "",
        "onizleme_png": None,
        "hata": None,
        "mast_name": None,
        "latitude": None,
        "longitude": None,
        "utm_east": None,
        "utm_north": None,
        "utm_zone": None,
        "elevation_m": None,
        "mast_height_m": None,
        "installation_date": None,
        "coordinate_system": None,
        "sensors": {},
        "serial_numbers": {},
        "confidence": {},
        "warnings": [],
        "source_pages": {},
    }

    def sayi(deger):
        if deger is None:
            return None
        try:
            return float(str(deger).strip().replace(" ", "").replace(",", "."))
        except Exception:
            return None

    def alan_yaz(alan, deger, sayfa_no=None, guven="Yüksek"):
        if deger is None or deger == "":
            return
        sonuc[alan] = deger
        sonuc["confidence"][alan] = guven
        if sayfa_no is not None:
            sonuc["source_pages"][alan] = sayfa_no

    try:
        import fitz
        globals()["fitz"] = fitz
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        sonuc["sayfa_sayisi"] = len(doc)
        sayfalar = []
        ilgili_sayfa_indeksi = 0

        for indeks, sayfa in enumerate(doc):
            sayfa_no = indeks + 1
            metin = (sayfa.get_text("text") or "").strip()
            tablo_metni = _pdf_tablo_metinleri(sayfa)
            birlesik = "\n".join(x for x in (metin, tablo_metni) if x).strip()

            # Yalnızca metin katmanı çok zayıfsa OCR çalıştırılır.
            if len(re.sub(r"\s+", "", birlesik)) < 40:
                ocr = _pdf_sayfa_ocr(sayfa)
                if ocr:
                    birlesik = "\n".join(x for x in (birlesik, ocr) if x).strip()

            norm = re.sub(r"[\t\r]+", " ", birlesik)
            norm = re.sub(r"[ ]+", " ", norm)
            sayfalar.append({"no": sayfa_no, "text": birlesik, "norm": norm})

            if re.search(
                r"coordinates? of the met mast|coordinate system\s+east/x\s+north/y|"
                r"photo-documentation of the mast and sensors|calibrations and post-correction",
                norm,
                re.I,
            ):
                ilgili_sayfa_indeksi = indeks

        sonuc["metin"] = "\n".join(
            f"\n--- SAYFA {p['no']} ---\n{p['text']}" for p in sayfalar
        ).strip()

        if len(doc):
            pix = doc[ilgili_sayfa_indeksi].get_pixmap(
                matrix=fitz.Matrix(1.35, 1.35), alpha=False
            )
            sonuc["onizleme_png"] = pix.tobytes("png")
        doc.close()
    except Exception as hata:
        sonuc["hata"] = str(hata)
        return sonuc

    if not sayfalar:
        sonuc["warnings"].append("PDF içerisinde okunabilir sayfa bulunamadı.")
        return sonuc

    tum_metin = "\n".join(p["norm"] for p in sayfalar)

    # ------------------------------------------------------------
    # DİREK ADI VE KURULUM TARİHİ
    # ------------------------------------------------------------
    for p in sayfalar:
        desenler = [
            r"working title of the station is\s*[“\"']?([^\n”\"']+)",
            r"Project Details\s+Site:\s*([^,\n]+)",
            r"measurement campaign started[^\n]*?at the site of\s+([^\.\n]+)",
        ]
        for desen in desenler:
            m = re.search(desen, p["norm"], re.I)
            if m:
                ad = m.group(1).strip(" :-–—.\"'“”")
                if 2 <= len(ad) <= 80:
                    alan_yaz("mast_name", ad, p["no"])
                    break
        if sonuc["mast_name"]:
            break

    for p in sayfalar:
        m = re.search(
            r"Commissioning\s*Date\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
            p["norm"], re.I,
        )
        if not m:
            m = re.search(
                r"(?:mast installation|installation|commissioning|erection)[^\n]{0,80}?"
                r"(?:on\s+)?(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
                p["norm"], re.I,
            )
        if m:
            alan_yaz("installation_date", m.group(1), p["no"])
            break

    # ------------------------------------------------------------
    # KOORDİNATLAR
    # East/X = boylam, North/Y = enlem. Öncelik koordinat tablosudur.
    # ------------------------------------------------------------
    koordinat_sayfalari = [
        p for p in sayfalar
        if re.search(
            r"coordinates? of the met mast|coordinate system\s+east/x\s+north/y|"
            r"measurement site",
            p["norm"], re.I,
        )
    ]

    for p in koordinat_sayfalari:
        t = p["norm"]

        # Örnek: Geographic decimal WGS84 27.69383 41.13815 3m 169
        geo = re.search(
            r"Geographic\s+decimal\s+(WGS\s*84|ED\s*50|ITRF\s*\d{2,4})\s+"
            r"(-?\d{1,3}[.,]\d{4,10})\s+(-?\d{1,2}[.,]\d{4,10})"
            r"(?:\s+\d+(?:[.,]\d+)?\s*m)?(?:\s+(-?\d{1,4}(?:[.,]\d+)?))?",
            t, re.I,
        )
        if geo:
            datum = re.sub(r"\s+", "", geo.group(1).upper())
            datum = "WGS84" if datum == "WGS84" else datum
            alan_yaz("longitude", sayi(geo.group(2)), p["no"])
            alan_yaz("latitude", sayi(geo.group(3)), p["no"])
            alan_yaz("coordinate_system", f"Geographic decimal {datum}", p["no"])
            if geo.group(4):
                alan_yaz("elevation_m", sayi(geo.group(4)), p["no"])

        # Satır sonları tablo hücrelerini bölebilir. UTM, zone, East ve North sırayla aranır.
        utm = re.search(
            r"UTM\s*(?:WGS\s*)?(\d{1,2}\s*[C-HJ-NP-X]?)\s+"
            r"(\d{5,7}(?:[.,]\d+)?)\s+(\d{6,8}(?:[.,]\d+)?)",
            t, re.I,
        )
        if not utm:
            utm = re.search(
                r"UTM\s+WGS\s*\n?\s*(\d{1,2}\s*[C-HJ-NP-X]?)\s+"
                r"(\d{5,7}(?:[.,]\d+)?)\s+(\d{6,8}(?:[.,]\d+)?)",
                t, re.I,
            )
        if utm:
            alan_yaz("utm_zone", re.sub(r"\s+", " ", utm.group(1).strip()).upper(), p["no"])
            alan_yaz("utm_east", sayi(utm.group(2)), p["no"])
            alan_yaz("utm_north", sayi(utm.group(3)), p["no"])

        # Genel tablo biçimi: WGS84 27.x 41.x ... UTM WGS 35 T 558... 455...
        if sonuc["longitude"] is None or sonuc["latitude"] is None:
            geo2 = re.search(
                r"WGS\s*84\s+(-?\d{1,3}[.,]\d{4,10})\s+"
                r"(-?\d{1,2}[.,]\d{4,10})",
                t, re.I,
            )
            if geo2:
                alan_yaz("longitude", sayi(geo2.group(1)), p["no"])
                alan_yaz("latitude", sayi(geo2.group(2)), p["no"])
                if not sonuc["coordinate_system"]:
                    alan_yaz("coordinate_system", "Geographic decimal WGS84", p["no"])

        if sonuc["elevation_m"] is None:
            em = re.search(r"Elevation\s*\[?m\]?[^\n]{0,80}?(-?\d{1,4}(?:[.,]\d+)?)", t, re.I)
            if em:
                alan_yaz("elevation_m", sayi(em.group(1)), p["no"], "Orta")

    # Fotoğraf açıklamasındaki koordinat çifti yedek doğrulamadır: (boylam, enlem)
    if sonuc["latitude"] is None or sonuc["longitude"] is None:
        for p in sayfalar:
            m = re.search(
                r"met mast location\s*\(\s*(-?\d{1,3}[.,]\d{4,10})\s*,\s*"
                r"(-?\d{1,2}[.,]\d{4,10})\s*\)",
                p["norm"], re.I,
            )
            if m:
                alan_yaz("longitude", sayi(m.group(1)), p["no"], "Orta")
                alan_yaz("latitude", sayi(m.group(2)), p["no"], "Orta")
                break

    # ------------------------------------------------------------
    # DİREK YÜKSEKLİĞİ
    # Sensör yüksekliği ile direk yüksekliği karıştırılmaz.
    # ------------------------------------------------------------
    for p in sayfalar:
        m = re.search(
            r"tower\s+top\s+height[\s\S]{0,120}?\bis\s*(\d{1,3}(?:[.,]\d+)?)\s*m\b",
            p["norm"], re.I,
        )
        if not m:
            m = re.search(
                r"(?:meteorological\s+mast|mast|tower)[^\n]{0,80}?"
                r"(?:total\s+)?height\s*[:\-]?\s*(\d{1,3}(?:[.,]\d+)?)\s*m\b",
                p["norm"], re.I,
            )
        if m:
            alan_yaz("mast_height_m", sayi(m.group(1)), p["no"])
            break

    # ------------------------------------------------------------
    # SENSÖR YÜKSEKLİKLERİ
    # v1-v4 anemometreleri WS1-WS4'e, dir1-dir2 yön sensörlerine eşlenir.
    # ------------------------------------------------------------
    sensor_esleme = {
        "WS1_Avg": [r"(?:anemometer|anemometre)[^\n]{0,80}?\(?v\s*1\)?[^\n]{0,80}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m",
                    r"top\s+anemometer[^\n]{0,100}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m"],
        "WS2_Avg": [r"(?:anemometer|anemometre)[^\n]{0,80}?\(?v\s*2\)?[^\n]{0,80}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m",
                    r"backup\s+anemometer[^\n]{0,100}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m"],
        "WS3_Avg": [r"(?:anemometer|anemometre)[^\n]{0,80}?\(?v\s*3\)?[^\n]{0,80}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m"],
        "WS4_Avg": [r"(?:anemometer|anemometre)[^\n]{0,80}?\(?v\s*4\)?[^\n]{0,80}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m"],
        "WD1_Avg": [r"(?:wind\s*vane|direction\s*sensor)[^\n]{0,80}?\(?dir\s*1\)?[^\n]{0,80}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m",
                    r"top\s+wind\s+vane[^\n]{0,100}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m"],
        "WD2_Avg": [r"(?:wind\s*vane|direction\s*sensor)[^\n]{0,80}?\(?dir\s*2\)?[^\n]{0,80}?at\s*(\d{1,3}(?:[.,]\d+)?)\s*m"],
    }

    for kolon, desenler in sensor_esleme.items():
        for p in sayfalar:
            bulundu = None
            for desen in desenler:
                m = re.search(desen, p["norm"], re.I)
                if m:
                    h = sayi(m.group(1))
                    if h is not None and 1 <= h <= 300:
                        bulundu = h
                        break
            if bulundu is not None:
                sonuc["sensors"][kolon] = bulundu
                sonuc["confidence"][kolon] = "Yüksek"
                sonuc["source_pages"][kolon] = p["no"]
                break

    # Wind Vane offset tablosu, fotoğraf açıklaması bulunamazsa WD değerlerini tamamlar.
    for p in sayfalar:
        t = p["norm"]
        if not re.search(r"Wind\s+Vane\s+offset", t, re.I):
            continue
        for no, kolon in ((1, "WD1_Avg"), (2, "WD2_Avg")):
            if kolon in sonuc["sensors"]:
                continue
            m = re.search(
                rf"Wind\s+Vane\s*{no}\s+(\d{{1,3}}(?:[.,]\d+)?)\s*m",
                t, re.I,
            )
            if m:
                sonuc["sensors"][kolon] = sayi(m.group(1))
                sonuc["confidence"][kolon] = "Yüksek"
                sonuc["source_pages"][kolon] = p["no"]

    # Kalibrasyon tablosundaki seri numaralarını ve yükseklikleri ek doğrulama olarak al.
    for p in sayfalar:
        t = p["norm"]
        if not re.search(r"Calibrations? and Post-Correction|Mast\s+.*height", t, re.I):
            continue

        # TFC adv. <serial> <height> biçimi
        ws_rows = re.findall(
            r"TFC\s*adv\.?\s+(\d{6,12})\s+(83(?:[.,]0)?|78[.,]5|60(?:[.,]0)?|40(?:[.,]0)?)\b",
            t, re.I,
        )
        for idx, (serial, htxt) in enumerate(ws_rows[:4], start=1):
            kolon = f"WS{idx}_Avg"
            sonuc["serial_numbers"].setdefault(kolon, serial)
            if kolon not in sonuc["sensors"]:
                sonuc["sensors"][kolon] = sayi(htxt)
                sonuc["confidence"][kolon] = "Yüksek"
                sonuc["source_pages"][kolon] = p["no"]

        # TFC <serial> 78.5 / 40 biçimi yön sensörleri
        wd_rows = re.findall(
            r"(?<!adv\.\s)TFC\s+(\d{6,12})\s+(78[.,]5|40(?:[.,]0)?)\b",
            t, re.I,
        )
        for idx, (serial, htxt) in enumerate(wd_rows[:2], start=1):
            kolon = f"WD{idx}_Avg"
            sonuc["serial_numbers"].setdefault(kolon, serial)
            if kolon not in sonuc["sensors"]:
                sonuc["sensors"][kolon] = sayi(htxt)
                sonuc["confidence"][kolon] = "Yüksek"
                sonuc["source_pages"][kolon] = p["no"]

    # Son kontroller
    if sonuc["latitude"] is not None and not (-90 <= sonuc["latitude"] <= 90):
        sonuc["warnings"].append("Enlem değeri geçersiz görünüyor.")
    if sonuc["longitude"] is not None and not (-180 <= sonuc["longitude"] <= 180):
        sonuc["warnings"].append("Boylam değeri geçersiz görünüyor.")

    gerekli = ["WS1_Avg", "WS2_Avg", "WS3_Avg", "WS4_Avg", "WD1_Avg", "WD2_Avg"]
    eksik = [k for k in gerekli if k not in sonuc["sensors"]]
    if eksik:
        sonuc["warnings"].append(
            "Raporda bulunamayan sensör yükseklikleri 0 bırakıldı: " + ", ".join(eksik)
        )

    if sonuc["latitude"] is None or sonuc["longitude"] is None:
        sonuc["warnings"].append("Direk koordinatları otomatik bulunamadı; elle doğrulayın.")

    return sonuc

def rapor_kaydini_veri_setine_uygula(veri_seti_adi, rapor_kaydi):
    """Onaylanan kurulum raporu bilgisini oturum kayıtlarına uygular."""
    app_state.setdefault("mast_registry", {})
    app_state["mast_registry"][veri_seti_adi] = rapor_kaydi
    app_state.setdefault("sensor_heights", {})
    mevcut = app_state["sensor_heights"].setdefault(veri_seti_adi, {k: 0.0 for k in RUZGAR_KOLONLARI})
    for kolon, yuk in rapor_kaydi.get("sensors", {}).items():
        if kolon in RUZGAR_KOLONLARI and yuk is not None:
            mevcut[kolon] = float(yuk)
            st.session_state[f"sensor_height::{veri_seti_adi}::{kolon}"] = float(yuk)

# LOGGERNET DOSYASINI OKUMA
# ============================================================

@st.cache_resource(show_spinner=False)
def _loggernet_okuma_kilidi():
    import threading
    return threading.RLock()


@st.cache_data(show_spinner=False, max_entries=12)
def loggernet_oku(dosya_bytes):
    with _loggernet_okuma_kilidi():
        """LoggerNet TOA5 veya standart CSV WindData dosyasını güvenli biçimde okur.

        Header satırı sabit kabul edilmez; ilk satırlarda TIMESTAMP aranır. Böylece
        farklı LoggerNet export şablonları ve BOM içeren dosyalar aynı okuyucudan geçer.
        """
        from io import BytesIO

        if isinstance(dosya_bytes, bytes):
            metin = dosya_bytes.decode("utf-8-sig", errors="replace")
        else:
            metin = str(dosya_bytes)

        # Read only the header prefix; avoid retaining a list of every text row.
        import itertools
        satirlar = []
        _start = 0
        for _line_end in itertools.islice(re.finditer(r'\r\n|\r|\n', metin), 12):
            satirlar.append(metin[_start:_line_end.start()])
            _start = _line_end.end()
        if len(satirlar) < 12 and _start < len(metin):
            satirlar.append(metin[_start:])
        header_idx = None
        for i, satir in enumerate(satirlar[:12]):
            if re.search(r'(^|[,;\t\"])(timestamp|date\s*time|datetime)([,;\t\"]|$)', satir, re.I):
                header_idx = i
                break
        if header_idx is None:
            # Eski standart TOA5 yapısına geri dönüş.
            header_idx = 1 if len(satirlar) > 1 else 0

        # LoggerNet TOA5 esas olarak virgüllüdür. Standart CSV/TXT için ayırıcıyı
        # header satırından seç; pandas python engine quoted alanları korur.
        header_line = satirlar[header_idx] if header_idx < len(satirlar) else ""
        if ';' in header_line and header_line.count(';') > header_line.count(','):
            sep = ';'
        elif '\t' in header_line and header_line.count('\t') > header_line.count(','):
            sep = '\t'
        else:
            sep = ','

        # Convert bounded chunks before concatenating: retain numeric arrays rather
        # than millions of Python strings and the parser's full row list at once.
        parts = []
        _logger_first_rows = None
        _source = BytesIO(dosya_bytes if isinstance(dosya_bytes, bytes) else metin.encode('utf-8'))
        del metin, satirlar, header_line
        with pd.read_csv(_source, header=header_idx, sep=sep,
                         encoding='utf-8-sig', encoding_errors='replace',
                         engine='python', dtype=str, chunksize=4096) as reader:
            for part in reader:
                if _logger_first_rows is None:
                    _logger_first_rows = part.head(4).copy()
                for c in part.columns:
                    norm = re.sub(r'[^a-z0-9]+', '', str(c).lower())
                    if norm not in {'timestamp', 'datetime', 'dateandtime', 'date_time'}:
                        part[c] = pd.to_numeric(part[c], errors='coerce')
                parts.append(part)
        veri = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
        del parts
        if _logger_first_rows is None:
            _logger_first_rows = veri.head(4).copy()
        veri.columns = [str(k).strip().strip('"').lstrip('\ufeff') for k in veri.columns]

        # TIMESTAMP adının büyük/küçük harf veya DateTime varyasyonlarını normalize et.
        ts_kolonu = None
        for kolon in veri.columns:
            norm = re.sub(r'[^a-z0-9]+', '', str(kolon).lower())
            if norm in {'timestamp', 'datetime', 'dateandtime', 'date_time'}:
                ts_kolonu = kolon
                break
        if ts_kolonu is None:
            raise ValueError('TIMESTAMP/DateTime kolonu bulunamadı.')
        if ts_kolonu != 'TIMESTAMP':
            veri = veri.rename(columns={ts_kolonu: 'TIMESTAMP'})

        _logger_metadata = pd.Series(False, index=veri.index)
        _first_rows = _logger_first_rows.copy()
        _first_rows.columns = veri.columns
        if ts_kolonu != 'TIMESTAMP':
            _first_rows = _first_rows.rename(columns={ts_kolonu: 'TIMESTAMP'})
        _logger_metadata.loc[_first_rows.index] = (_first_rows['TIMESTAMP'].astype(str).eq('TS')
            | _first_rows.isin(['Avg','Smp','WVc','Std']).any(axis=1))
        veri['TIMESTAMP'] = pd.to_datetime(veri['TIMESTAMP'], errors='coerce')
        for kolon in [k for k in veri.columns if k != 'TIMESTAMP']:
            veri[kolon] = pd.to_numeric(veri[kolon], errors='coerce')

        _invalid_timestamp_count = int((veri['TIMESTAMP'].isna() & ~_logger_metadata).sum())
        veri = veri.dropna(subset=['TIMESTAMP']).sort_values('TIMESTAMP').reset_index(drop=True)
        veri.attrs["discarded_invalid_times"] = _invalid_timestamp_count
        if veri.empty:
            raise ValueError('Dosyada geçerli zaman damgalı kayıt bulunamadı.')
        measured = [c for c in veri.columns if re.fullmatch(r"WS\d+_Avg", str(c), re.I)]
        if not measured:
            raise ValueError("WS1_Avg benzeri hız kanalı bulunamadı. Dosyanın hız sütunları eşleştirilmelidir.")
        veri.attrs["measured_speed_columns"] = measured
        for c in RUZGAR_KOLONLARI:
            if c not in veri.columns:
                veri[c] = np.nan  # Ölçüm olmayan kanal; gerçek veri üretilmez.
        return veri



@st.cache_data(show_spinner=False, max_entries=12)
def loggernet_oku_yoldan(dosya_yolu, mtime_ns, dosya_boyutu):
    """Yerel LoggerNet dosyasını aynı esnek okuyucuyla ve dosya imzasıyla cache'li okur."""
    # Keep one parsed-frame cache for paths; do not also populate the bytes cache.
    return getattr(loggernet_oku, '__wrapped__', loggernet_oku)(Path(dosya_yolu).read_bytes())


# ============================================================
# HIZLI TEMİZLEME
# ============================================================

@st.cache_data(show_spinner=False, max_entries=16)

def _qc_monthly_table(timestamps, raw_values, usable_values):
    """Aylık ölçüm istatistikleri; boşluk doldurma yapılmaz."""
    q=pd.DataFrame({"ts":pd.to_datetime(timestamps,errors="coerce"),"raw":pd.to_numeric(raw_values,errors="coerce"),"valid":pd.to_numeric(usable_values,errors="coerce")})
    q=q.dropna(subset=["ts"]).sort_values("ts")
    q["period"]=q["ts"].dt.to_period("M")
    rows=[]
    first_ts=q["ts"].min()
    last_ts=q["ts"].max()
    for period,g in q.groupby("period",sort=True):
        x=g["valid"].dropna()
        observed=int(g["ts"].nunique())
        valid=int(g.loc[g["valid"].notna(),"ts"].nunique())
        interval_start=max(period.start_time,first_ts)
        interval_end=min(period.end_time.floor("10min"),last_ts)
        possible=int((interval_end-interval_start).total_seconds()//600)+1
        rows.append({"Yıl":int(period.year),"Ay":int(period.month),"Beklenen kayıt (dönem)":possible,"Mevcut kayıt":observed,"Geçerli kayıt":valid,"DCR (%)":round(100*observed/possible,2),"DRR (%)":round(100*valid/observed,2) if observed else np.nan,"Ortalama (m/s)":x.mean(),"Medyan (m/s)":x.median(),"Min (m/s)":x.min(),"Maks (m/s)":x.max(),"Std. sapma (m/s)":x.std(ddof=1)})
    return pd.DataFrame(rows)


def _qc_read_windographer(content):
    """Windographer Export Table: tab ayrılmış Monthly Statistics."""
    from io import StringIO
    txt=content.decode("utf-8-sig",errors="replace")
    lines=[l for l in txt.splitlines() if l.strip()]
    header=next((i for i,l in enumerate(lines) if "Year" in l and "Month" in l and "Possible" in l),None)
    if header is None:
        raise ValueError("Year/Month/Possible başlıkları bulunamadı")
    months={m:i+1 for i,m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}
    result=[]
    for line in lines[header+1:]:
        cells=line.split("\t")
        if len(cells)<10:continue
        try:
            ix=next(i for i,c in enumerate(cells[:3]) if c.strip().isdigit() and len(c.strip())==4)
            year=int(cells[ix]); month=months[cells[ix+1].strip()[:3].title()]
            # Index after Year: Month, Timesteps, Possible, Valid, DCR, DRR, Mean.
            possible=int(cells[ix+3].replace(",","")); valid=int(cells[ix+4].replace(",","")); mean=float(cells[ix+7].replace(",",""))
            result.append({"Yıl":year,"Ay":month,"WG Possible":possible,"WG Valid":valid,"WG Ortalama (m/s)":mean})
        except (ValueError,IndexError,StopIteration,KeyError):
            continue
    if not result:raise ValueError("Aylık satırlar ayrıştırılamadı")
    return pd.DataFrame(result)

KALITE_MOTOR_SURUMU = "general-qc-v1"


def hiz_sensor_kolonlari(veri):
    original = veri.attrs.get("measured_speed_columns")
    return [c for c in veri.columns if re.fullmatch(r"WS\d+_Avg", str(c), re.I)
            and (original is None or c in original)]


def olcum_zaman_kontrolu(veri):
    ts = pd.to_datetime(veri["TIMESTAMP"], errors="coerce")
    diffs = ts.dropna().sort_values().diff().dt.total_seconds()
    positive = diffs[diffs > 0]
    step = float(positive.mode().iloc[0]) if not positive.empty else np.nan
    duplicate = int(ts.dropna().duplicated().sum())
    cadence_ok = bool(np.isfinite(step) and step > 0 and len(positive) >= 5
                      and ((positive / step - np.round(positive / step)).abs() < 1e-6).mean() >= 1.0)
    return {"step_seconds":step,"duplicates":duplicate,"invalid_times":int(ts.isna().sum())+int(veri.attrs.get("discarded_invalid_times",0)),"cadence_ok":cadence_ok}


@st.cache_data(show_spinner=False, max_entries=8)
def otomatik_olcum_kontrolu(veri):
    """Ortak ön kontrol kuralları. Ham girdi korunur; sıfır tek başına dışlama nedeni değildir.

    Bir saat / 0,25 m/s / 2 m/s eşikleri uygulama içi tarama tercihleridir;
    IEC/MEASNET sertifikasyonu veya tam otomatik arıza teşhisi değildir.
    """
    sensors = hiz_sensor_kolonlari(veri)
    time = olcum_zaman_kontrolu(veri)
    step = time["step_seconds"]
    mask = pd.DataFrame(False,index=veri.index,columns=sensors)
    reasons = pd.DataFrame("Geçerli ölçüm",index=veri.index,columns=sensors)
    ts = pd.to_datetime(veri["TIMESTAMP"],errors="coerce")
    values = veri[sensors].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan)
    events=[]
    for c in sensors:
        invalid=values[c].isna() | ~values[c].between(0,45)
        mask[c]=invalid
        reasons.loc[invalid,c]="Eksik / fiziksel sınır dışı"
    if not time["cadence_ok"] or time["duplicates"]:
        return mask,reasons,pd.DataFrame(events),time
    ordered_index=ts.sort_values().index
    for c in sensors:
        v=values.loc[ordered_index,c];t=ts.loc[ordered_index]
        peers=[p for p in sensors if p!=c]
        if len(peers)<2:continue
        pv=values.loc[ordered_index,peers].where(values.loc[ordered_index,peers].ge(0)&values.loc[ordered_index,peers].le(45))
        support=pv.gt(2).sum(axis=1)>=2
        candidate=v.between(0,.25)
        groups=((candidate!=candidate.shift())|(t.diff().dt.total_seconds()!=step)).cumsum()
        segments=pd.DataFrame({"group":groups,"candidate":candidate,"support":support})
        grouped=segments[candidate].groupby("group").agg(n=("candidate","size"),support=("support","mean"))
        for gid in grouped.index[(grouped.n>=6)&(grouped.n*step>=3600)&(grouped.support>=.8)]:
            idx=v.index[(groups==gid)&candidate]
            kind="Uzun süre sıfıra yakın; diğer iki sensörde rüzgâr var"
            mask.loc[idx,c]=True;reasons.loc[idx,c]=kind
            events.append({"Sensör":c,"Başlangıç":t.loc[idx].min(),"Bitiş":t.loc[idx].max(),"Kayıt":len(idx),"Neden":kind})
        flat_groups=((v.diff().abs()>.001)|v.isna()|v.shift().isna()|(t.diff().dt.total_seconds()!=step)).cumsum()
        counts=v.groupby(flat_groups).size()
        eligible=counts.index[(counts>=6)&(counts*step>=3600)]
        for gid in eligible:
            idx=v.index[flat_groups==gid]
            z=v.loc[idx]
            if z.isna().any() or z.mean()<=.25:continue
            if z.max()-z.min()<=.001 and support.loc[idx].mean()>=.8 and pv.loc[idx].std().gt(.3).sum()>=2:
                kind="Sabit sensör; diğer iki sensör değişiyor"
                mask.loc[idx,c]=True;reasons.loc[idx,c]=kind
                events.append({"Sensör":c,"Başlangıç":t.loc[idx].min(),"Bitiş":t.loc[idx].max(),"Kayıt":len(idx),"Neden":kind})
    return mask,reasons,pd.DataFrame(events),time


def olcum_kalite_verisi(veri,veri_seti_adi):
    """Fiziksel kontrol, otomatik kalite işaretleri ve manuel işaretler; tahmin eklenmez."""
    out=veri.copy(deep=True)
    full=globals().get("tum_veri_setleri",{}).get(veri_seti_adi,veri)
    _,_,episodes,_=otomatik_olcum_kontrolu(full)
    ts=pd.to_datetime(out["TIMESTAMP"],errors="coerce")
    for c in hiz_sensor_kolonlari(out):
        v=pd.to_numeric(out[c],errors="coerce")
        exclude=v.isna()|~np.isfinite(v)|~v.between(0,45)
        if not episodes.empty:
            for event in episodes[episodes["Sensör"]==c].to_dict("records"):
                exclude|=ts.between(event["Başlangıç"],event["Bitiş"])
        for mark in st.session_state.get("qc_flags_"+str(veri_seti_adi)+"_"+c,[]):
            exclude|=ts.between(pd.Timestamp(mark["from"]),pd.Timestamp(mark["to"]))
        out[c]=v.mask(exclude)
    return out


@st.cache_data(show_spinner=False,max_entries=16)
def olcum_kapsama_raporu(raw,clean,ref):
    timing=olcum_zaman_kontrolu(raw);step=timing["step_seconds"]
    rows=[]
    if not timing["cadence_ok"] or raw.empty or ref not in clean:
        return pd.DataFrame(),{**timing,"annual_ok":False,"period_ok":False,"longest_gap_hours":np.nan}
    start=pd.to_datetime(raw.TIMESTAMP).min();end=pd.to_datetime(raw.TIMESTAMP).max()
    count=int((end-start).total_seconds()/step)+1
    if count>2_000_000:
        return pd.DataFrame(),{**timing,"annual_ok":False,"period_ok":False,"longest_gap_hours":np.nan}
    expected=pd.date_range(start,end,freq=pd.Timedelta(seconds=step))
    valid_ts=pd.to_datetime(clean.loc[clean[ref].notna(),"TIMESTAMP"])
    valid_mask=pd.Series(expected.isin(valid_ts),index=expected)
    absent=~valid_mask;blocks=absent.ne(absent.shift()).cumsum()
    maxgap=float(absent[absent].groupby(blocks[absent]).size().max()*step/3600) if absent.any() else 0.
    for month,g in valid_mask.groupby(valid_mask.index.to_period("M")):
        rows.append({"Dönem":str(month),"Beklenen kayıt":len(g),"Geçerli gerçek ölçüm":int(g.sum()),
                     "Geçerli ölçüm (%)":float(100*g.mean()),"Eksik / dışlanan":int((~g).sum())})
    table=pd.DataFrame(rows)
    cadence=timing["cadence_ok"] and timing["duplicates"]==0 and timing["invalid_times"]==0
    month_ok=bool(table["Geçerli ölçüm (%)"].ge(90).all())
    year_span=(end-start).total_seconds()+step>=365*86400
    return table,{**timing,"annual_ok":bool(cadence and month_ok and maxgap<=2 and year_span),
                  "period_ok":bool(cadence and valid_mask.any()),"longest_gap_hours":maxgap,
                  "coverage_pct":float(100*valid_mask.mean()),"valid_count":int(valid_mask.sum()),"expected_count":len(valid_mask)}


def enerji_shear_hesapla(clean,heights):
    sensors=[c for c in hiz_sensor_kolonlari(clean) if float(heights.get(c,0) or 0)>0]
    if len(sensors)<2:return np.nan,0
    paired=clean[sensors].replace([np.inf,-np.inf],np.nan).dropna()
    if len(paired)<30:return np.nan,len(paired)
    h=np.array([float(heights[c]) for c in sensors]);v=paired[sensors].mean().to_numpy()
    good=(h>0)&np.isfinite(h)&(v>0)&np.isfinite(v)
    if good.sum()<2 or len(np.unique(h[good]))<2:return np.nan,len(paired)
    alpha,_=np.polyfit(np.log(h[good]),np.log(v[good]),1)
    return (float(alpha) if np.isfinite(alpha) else np.nan),len(paired)


def enerji_kalite_durumu(raw,name,heights):
    clean=olcum_kalite_verisi(raw,name)
    sensors=[c for c in hiz_sensor_kolonlari(raw) if np.isfinite(float(heights.get(c,0) or 0)) and float(heights.get(c,0) or 0)>0]
    if not sensors:return clean,None,pd.DataFrame(),{"period_ok":False,"annual_ok":False,"longest_gap_hours":np.nan}
    ref=max(sensors,key=lambda c:float(heights[c]))
    table,status=olcum_kapsama_raporu(raw,clean,ref)
    return clean,ref,table,status


@st.cache_data(show_spinner=False,max_entries=8)
def tamamlama_blok_testi(clean,target,reference,block_days,power_curve=None):
    """Deneme modeli. Test blokları eğitimden çıkarılır, iki yanında 7 gün tampon vardır.
    Sonuçlar hız hatasını gösterir; tahminin AEP açısından doğrulandığı anlamına gelmez.
    """
    q=clean[["TIMESTAMP",target,reference]].copy().sort_values("TIMESTAMP")
    q=q.dropna().loc[lambda z:z[target].gt(.25)&z[reference].gt(.25)]
    result=[]
    if len(q)<100 or q.TIMESTAMP.max()-q.TIMESTAMP.min()<pd.Timedelta(days=3*block_days):
        return pd.DataFrame(),None
    step=olcum_zaman_kontrolu(clean)["step_seconds"]
    if not np.isfinite(step):return pd.DataFrame(),None
    first=q.TIMESTAMP.min().normalize();last=q.TIMESTAMP.max()
    for a in pd.date_range(first,last-pd.Timedelta(days=block_days),freq=f"{block_days}D"):
        b=a+pd.Timedelta(days=block_days)
        test=q[q.TIMESTAMP.ge(a)&q.TIMESTAMP.lt(b)]
        train=q[~(q.TIMESTAMP.ge(a-pd.Timedelta(days=7))&q.TIMESTAMP.lt(b+pd.Timedelta(days=7)))]
        if len(test)<.90*block_days*86400/step or len(train)<90*86400/step or train[reference].std()<.1:continue
        slope,intercept=np.polyfit(train[reference],train[target],1)
        pred=slope*test[reference]+intercept;err=pred-test[target]
        row={"Test başlangıcı":a,"Test bitişi":b-pd.Timedelta(seconds=step),"Kayıt":len(test),
             "Ortalama sapma (%)":float(100*err.mean()/test[target].mean()),"MAE (m/s)":float(err.abs().mean()),
             "RMSE (m/s)":float(np.sqrt((err**2).mean())),"Gerçek ortalama":float(test[target].mean()),"Tahmin ortalama":float(pred.mean())}
        if power_curve is not None:
            speed=np.asarray(power_curve["wind_speed"],dtype=float)
            power=np.asarray(power_curve["power_kw"],dtype=float)
            measured_power=np.interp(test[target].to_numpy(),speed,power,left=0,right=0)
            estimated_power=np.interp(pred.to_numpy(),speed,power,left=0,right=0)
            row["Güç eğrisi enerji sapması (%)"]=(float(100*(estimated_power.sum()/measured_power.sum()-1)) if measured_power.sum()>0 else np.nan)
        result.append(row)
    if len(result)<3:return pd.DataFrame(result),None
    slope,intercept=np.polyfit(q[reference],q[target],1)
    if not np.isfinite(slope) or not np.isfinite(intercept) or slope<=0:return pd.DataFrame(result),None
    return pd.DataFrame(result),{"slope":float(slope),"intercept":float(intercept),"training_count":len(q),
                                 "reference_min":float(q[reference].min()),"reference_max":float(q[reference].max())}


def tamamlama_aday_verisi(clean,target,reference,model):
    out=clean[["TIMESTAMP",target,reference]].copy()
    out["Kaynak"]="Gerçek ölçüm"
    out.loc[out[target].isna(),"Kaynak"]="Eksik"
    # Referans aralığı dışında tahmin yapılmaz; adaylar ayrı dosyada korunur.
    eligible=out[target].isna()&out[reference].between(model["reference_min"],model["reference_max"])
    predicted=model["slope"]*out[reference]+model["intercept"]
    eligible&=predicted.between(0,45)
    out.loc[eligible,target]=predicted[eligible]
    out.loc[eligible,"Kaynak"]="Tahmini aday · enerji girdisi değil"
    return out


def kalite_isaretlerini_sakla():
    app_state["quality_flags"] = {
        k: list(st.session_state[k]) for k in st.session_state
        if str(k).startswith("qc_flags_") and isinstance(st.session_state[k], list)
    }
    return kalici_durumu_kaydet(app_state)


def kalite_onay_imzasi(veri, veri_seti_adi, yukseklikler):
    """Onay yalnızca incelenen veri, dönem, sensör ayarları ve işaretler için geçerlidir."""
    h = hashlib.sha256()
    h.update(pd.util.hash_pandas_object(veri, index=True).values.tobytes())
    full = globals().get("tum_veri_setleri",{}).get(veri_seti_adi,veri)
    _, _, auto_events, _ = otomatik_olcum_kontrolu(full)
    h.update(auto_events.to_json(date_format="iso").encode("utf-8"))
    isaretler = {k: st.session_state.get("qc_flags_" + str(veri_seti_adi) + "_" + k, [])
                for k in hiz_sensor_kolonlari(veri)}
    bilgi = {"method": KALITE_MOTOR_SURUMU, "mast": veri_seti_adi,
             "columns": list(veri.columns), "heights": yukseklikler, "flags": isaretler,
             "start": app_state.get("date_start"), "end": app_state.get("date_end")}
    h.update(json.dumps(bilgi, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8"))
    return h.hexdigest()


def enerji_verisi_hesaplanabilir(veri, veri_seti_adi, yukseklikler):
    """User review is optional; retain measured-data and time-axis checks for calculations."""
    _, _, _, status = enerji_kalite_durumu(veri, veri_seti_adi, yukseklikler)
    return bool(status["period_ok"])


def sensor_donem_incelemesi(veri, ust_kolon, alt_kolon):
    """Yıl-ay bazında ortak geçerli zamanlar; düşük hızlar teşhistir, otomatik silinmez."""
    q = veri[["TIMESTAMP", ust_kolon, alt_kolon]].copy()
    q["TIMESTAMP"] = pd.to_datetime(q["TIMESTAMP"], errors="coerce")
    for c in [ust_kolon, alt_kolon]:
        q[c] = pd.to_numeric(q[c], errors="coerce").replace([np.inf, -np.inf], np.nan)
        q[c] = q[c].where(q[c].between(0, 45))
    q = q.dropna(subset=["TIMESTAMP"])
    q["Dönem"] = q["TIMESTAMP"].dt.to_period("M")
    rows = []
    for donem, g in q.groupby("Dönem", sort=True):
        pair = g.dropna(subset=[ust_kolon, alt_kolon])
        u, a = pair[ust_kolon], pair[alt_kolon]
        rows.append({"Dönem": str(donem), "Üst sensör geçerli kayıt": int(g[ust_kolon].notna().sum()),
                     "Alt sensör geçerli kayıt": int(g[alt_kolon].notna().sum()),
                     "Eşzamanlı kayıt": len(pair), "Üst ortalama (m/s)": u.mean(),
                     "Alt ortalama (m/s)": a.mean(), "Üst / alt ortalama": u.mean()/a.mean() if len(pair) and a.mean()>0 else np.nan,
                     "Üst sensör sıfır (%)": float(100*u.eq(0).mean()) if len(pair) else np.nan,
                     "Üst daha düşük (%)": float(100*(u<a).mean()) if len(pair) else np.nan})
    return pd.DataFrame(rows)


def hizli_temizle(veri, sensor_yukseklikleri=(0.0, 0.0, 0.0, 0.0)):
    """
    İlk hızlı sürüm:

    1. Negatif değerleri siler.
    2. 45 m/s üzerindeki değerleri siler.
    3. Bir saat boyunca değişmeyen sensörü şüpheli sayar.
    4. Diğer sensörlerin medyanından 5 m/s fazla uzaklaşan
       değerleri şüpheli sayar.
    5. Eksik değerleri yükseklik olarak en yakın sensörden,
       alpha=0.14 kullanarak tamamlar.

    Satır satır apply kullanılmadığı için önceki sürümden
    çok daha hızlıdır.
    """

    temiz = veri.copy()

    kalite = pd.DataFrame(
        index=temiz.index
    )

    # --------------------------------------------------------
    # Temel fiziksel kontrol
    # --------------------------------------------------------

    for kolon in RUZGAR_KOLONLARI:
        kalite[kolon] = "Sağlıklı"

        gecersiz = (
            temiz[kolon].isna()
            | (temiz[kolon] < 0)
            | (temiz[kolon] > 45)
        )

        kalite.loc[gecersiz, kolon] = (
            "Eksik veya fiziksel olarak geçersiz"
        )

        temiz.loc[gecersiz, kolon] = np.nan

    # --------------------------------------------------------
    # Takılı kalma kontrolü
    # 6 adet 10 dakikalık kayıt yaklaşık 1 saattir.
    # --------------------------------------------------------

    for kolon in RUZGAR_KOLONLARI:
        hareketli_maksimum = (
            temiz[kolon]
            .rolling(window=6, min_periods=6)
            .max()
        )

        hareketli_minimum = (
            temiz[kolon]
            .rolling(window=6, min_periods=6)
            .min()
        )

        takili = (
            hareketli_maksimum
            - hareketli_minimum
        ) <= 0.01

        kalite.loc[takili, kolon] = (
            "Takılı kalma şüphesi"
        )

        temiz.loc[takili, kolon] = np.nan

    # --------------------------------------------------------
    # Sensörler arası çelişki kontrolü
    # --------------------------------------------------------

    sensor_medyani = temiz[
        RUZGAR_KOLONLARI
    ].median(axis=1)

    for kolon in RUZGAR_KOLONLARI:
        celiski = (
            temiz[kolon] - sensor_medyani
        ).abs() > 5.0

        kalite.loc[celiski, kolon] = (
            "Diğer sensörlerle çelişiyor"
        )

        temiz.loc[celiski, kolon] = np.nan

    # --------------------------------------------------------
    # Eksik değerlerin ekstrapolasyonla doldurulması
    # --------------------------------------------------------

    alpha = 0.14

    # Yükseklikler doğrudan seçili direğin kurulum raporu/ayar kaydından gelir.
    # 0, NaN veya negatif yükseklikler hesaplamaya kesinlikle sokulmaz.
    gelen_yukseklikler = list(sensor_yukseklikleri or ())
    if len(gelen_yukseklikler) < len(RUZGAR_KOLONLARI):
        gelen_yukseklikler += [0.0] * (len(RUZGAR_KOLONLARI) - len(gelen_yukseklikler))
    yukseklikler = {
        kolon: float(gelen_yukseklikler[i] or 0.0)
        for i, kolon in enumerate(RUZGAR_KOLONLARI)
    }
    gecerli_yukseklikli_sensorler = [
        kolon for kolon, yuk in yukseklikler.items()
        if np.isfinite(yuk) and yuk > 0
    ]

    for hedef_kolon in RUZGAR_KOLONLARI:
        hedef_yukseklik = yukseklikler.get(hedef_kolon, 0.0)
        if not np.isfinite(hedef_yukseklik) or hedef_yukseklik <= 0:
            kalite.loc[temiz[hedef_kolon].isna(), hedef_kolon] = (
                "Kurulum raporunda sensör yüksekliği bulunamadı"
            )
            continue

        eksik = temiz[hedef_kolon].isna()
        referans_sirasi = sorted(
            [
                kolon for kolon in gecerli_yukseklikli_sensorler
                if kolon != hedef_kolon
            ],
            key=lambda kolon: abs(yukseklikler[kolon] - hedef_yukseklik)
        )

        for referans_kolon in referans_sirasi:
            referans_yukseklik = yukseklikler.get(referans_kolon, 0.0)
            if not np.isfinite(referans_yukseklik) or referans_yukseklik <= 0:
                continue

            doldurulabilir = eksik & temiz[referans_kolon].notna()
            if not bool(doldurulabilir.any()):
                continue

            oran = hedef_yukseklik / referans_yukseklik
            if not np.isfinite(oran) or oran <= 0:
                continue

            temiz.loc[doldurulabilir, hedef_kolon] = (
                temiz.loc[doldurulabilir, referans_kolon] * (oran ** alpha)
            )
            kalite.loc[doldurulabilir, hedef_kolon] = (
                f"{sensor_etiketi(referans_kolon, yukseklikler)} "
                "sensöründen ekstrapole edildi"
            )
            eksik = temiz[hedef_kolon].isna()

    return temiz, kalite




# ============================================================
# YÜKSEK ÇÖZÜNÜRLÜKLÜ HALİHAZIR HARİTA / TOPOĞRAFYA MODÜLÜ
# ============================================================

def _topografya_sayisal_kolon_bul(kolonlar, adaylar):
    harita = {str(k).strip().lower(): k for k in kolonlar}
    for aday in adaylar:
        if aday.lower() in harita:
            return harita[aday.lower()]
    for kucuk, asil in harita.items():
        if any(a.lower() in kucuk for a in adaylar):
            return asil
    return None


def _topografya_csv_xyz_oku(dosya_bytes, dosya_adi):
    """CSV/TXT/XYZ kot noktalarını X-Y-Z tablosuna dönüştürür."""
    denemeler = [
        dict(sep=None, engine="python"),
        dict(sep=";"),
        dict(sep=","),
        dict(delim_whitespace=True),
    ]
    son_hata = None
    for kwargs in denemeler:
        try:
            df = pd.read_csv(io.BytesIO(dosya_bytes), **kwargs)
            if df.shape[1] >= 3:
                break
        except Exception as hata:
            son_hata = hata
            df = None
    if df is None or df.shape[1] < 3:
        raise ValueError(f"Kot noktası dosyası okunamadı: {son_hata or 'en az üç kolon gerekli'}")

    xk = _topografya_sayisal_kolon_bul(df.columns, ["x", "easting", "east", "utm_east", "boylam", "lon", "longitude"])
    yk = _topografya_sayisal_kolon_bul(df.columns, ["y", "northing", "north", "utm_north", "enlem", "lat", "latitude"])
    zk = _topografya_sayisal_kolon_bul(df.columns, ["z", "elevation", "elev", "height", "kot", "rakim", "altitude"])
    if not all([xk, yk, zk]):
        xk, yk, zk = list(df.columns[:3])
    out = pd.DataFrame({
        "X": pd.to_numeric(df[xk], errors="coerce"),
        "Y": pd.to_numeric(df[yk], errors="coerce"),
        "Z": pd.to_numeric(df[zk], errors="coerce"),
    }).dropna()
    out = out.replace([np.inf, -np.inf], np.nan).dropna()
    if len(out) < 3:
        raise ValueError("DEM üretmek için en az üç geçerli X-Y-Z noktası gerekir.")
    return out


def _topografya_landxml_oku(dosya_bytes):
    """LandXML içindeki CgPoint/Pnts kayıtlarını X-Y-Z olarak okur."""
    root = ET.fromstring(dosya_bytes)
    noktalar = []
    for eleman in root.iter():
        ad = eleman.tag.split("}")[-1]
        if ad not in {"CgPoint", "P"} or not (eleman.text or "").strip():
            continue
        parcalar = re.split(r"[\s,;]+", eleman.text.strip())
        sayilar = []
        for p in parcalar:
            try:
                sayilar.append(float(p))
            except Exception:
                pass
        if len(sayilar) >= 3:
            # LandXML çoğunlukla Northing Easting Elevation sırasındadır.
            noktalar.append((sayilar[1], sayilar[0], sayilar[2]))
    if len(noktalar) < 3:
        raise ValueError("LandXML içinde yeterli kot noktası bulunamadı.")
    return pd.DataFrame(noktalar, columns=["X", "Y", "Z"])


def _topografya_dxf_oku(dosya_bytes):
    """DXF POINT, 3D POLYLINE ve LWPOLYLINE vertex kotlarını okur."""
    try:
        import ezdxf
    except Exception as hata:
        raise RuntimeError("DXF okumak için 'ezdxf' paketi gerekli: pip install ezdxf") from hata
    gecici = Path.home() / ".maki_wind_studio" / "cache" / "topography_upload.dxf"
    gecici.parent.mkdir(parents=True, exist_ok=True)
    gecici.write_bytes(dosya_bytes)
    doc = ezdxf.readfile(str(gecici))
    msp = doc.modelspace()
    noktalar = []
    katmanlar = {}
    for e in msp:
        tip = e.dxftype()
        katman = getattr(e.dxf, "layer", "0")
        katmanlar[katman] = katmanlar.get(katman, 0) + 1
        try:
            if tip == "POINT":
                p = e.dxf.location
                noktalar.append((float(p.x), float(p.y), float(p.z)))
            elif tip == "POLYLINE":
                for v in e.vertices:
                    p = v.dxf.location
                    noktalar.append((float(p.x), float(p.y), float(p.z)))
            elif tip == "LWPOLYLINE":
                elev = float(getattr(e.dxf, "elevation", 0.0) or 0.0)
                for x, y, *_ in e.get_points():
                    noktalar.append((float(x), float(y), elev))
        except Exception:
            continue
    df = pd.DataFrame(noktalar, columns=["X", "Y", "Z"]).replace([np.inf, -np.inf], np.nan).dropna()
    if len(df) < 3:
        raise ValueError("DXF içinde Z değerli POINT/3D POLYLINE verisi bulunamadı.")
    return df, katmanlar


def _topografya_geotiff_ozeti(dosya_bytes):
    try:
        import rasterio
        from rasterio.io import MemoryFile
    except Exception as hata:
        raise RuntimeError("GeoTIFF okumak için 'rasterio' paketi gerekli: pip install rasterio") from hata
    with MemoryFile(dosya_bytes) as mem:
        with mem.open() as src:
            band = src.read(1, masked=True)
            gecerli = band.compressed()
            if gecerli.size == 0:
                raise ValueError("GeoTIFF içinde geçerli kot hücresi bulunamadı.")
            # Ekran önizlemesi için en fazla yaklaşık 250x250 hücre örnekle.
            adim_y = max(1, int(np.ceil(src.height / 250)))
            adim_x = max(1, int(np.ceil(src.width / 250)))
            ornek = band[::adim_y, ::adim_x].filled(np.nan)
            return {
                "tip": "GeoTIFF DEM",
                "genislik": int(src.width), "yukseklik": int(src.height),
                "crs": str(src.crs) if src.crs else "Tanımsız",
                "bounds": tuple(float(v) for v in src.bounds),
                "cozunurluk_x": float(abs(src.transform.a)),
                "cozunurluk_y": float(abs(src.transform.e)),
                "min_kot": float(np.nanmin(gecerli)),
                "max_kot": float(np.nanmax(gecerli)),
                "ortalama_kot": float(np.nanmean(gecerli)),
                "preview": ornek,
            }


def _topografya_nokta_dem_uret(noktalar, grid_m=5.0, max_hucre=220):
    """Kot noktalarından IDW tabanlı ön DEM üretir; mevcut modele dokunmaz."""
    pts = noktalar[["X", "Y", "Z"]].dropna().to_numpy(dtype=float)
    xmin, ymin = np.nanmin(pts[:, :2], axis=0)
    xmax, ymax = np.nanmax(pts[:, :2], axis=0)
    nx = int(np.clip(np.ceil((xmax-xmin)/max(float(grid_m), 0.1))+1, 20, max_hucre))
    ny = int(np.clip(np.ceil((ymax-ymin)/max(float(grid_m), 0.1))+1, 20, max_hucre))
    gx = np.linspace(xmin, xmax, nx)
    gy = np.linspace(ymin, ymax, ny)
    xx, yy = np.meshgrid(gx, gy)
    grid = np.full(xx.shape, np.nan, dtype=float)
    # Büyük nokta setlerinde hesap yükünü sınırlamak için düzenli örnekleme.
    if len(pts) > 5000:
        idx = np.linspace(0, len(pts)-1, 5000).astype(int)
        pts = pts[idx]
    for r in range(ny):
        dx = xx[r, :, None] - pts[None, :, 0]
        dy = yy[r, :, None] - pts[None, :, 1]
        d2 = dx*dx + dy*dy
        tam = d2 < 1e-12
        w = 1.0 / np.maximum(d2, 1e-6)
        vals = (w @ pts[:, 2]) / np.sum(w, axis=1)
        if tam.any():
            sat, sut = np.where(tam)
            for s in np.unique(sat):
                vals[s] = pts[sut[sat == s][0], 2]
        grid[r] = vals
    return gx, gy, grid




def _oda_file_converter_bul(kullanici_yolu=""):
    """Windows'ta ODA File Converter uygulamasını bulur."""
    adaylar = []
    if str(kullanici_yolu or "").strip():
        adaylar.append(Path(str(kullanici_yolu).strip().strip('"')))
    for env_name in ("ProgramFiles", "ProgramFiles(x86)"):
        kok = os.environ.get(env_name)
        if kok:
            adaylar.extend([
                Path(kok) / "ODA" / "ODAFileConverter" / "ODAFileConverter.exe",
                Path(kok) / "ODAFileConverter" / "ODAFileConverter.exe",
                Path(kok) / "Open Design Alliance" / "ODAFileConverter" / "ODAFileConverter.exe",
            ])
    for ad in ("ODAFileConverter.exe", "ODAFileConverter"):
        try:
            import shutil
            bulunan = shutil.which(ad)
            if bulunan:
                adaylar.append(Path(bulunan))
        except Exception:
            pass
    for aday in adaylar:
        try:
            if aday.is_file():
                return aday
        except Exception:
            continue
    return None


def _dwg_bytes_dxf_donustur(dosya_adi, dosya_bytes, converter_path=""):
    """DWG bytes içeriğini ODA File Converter ile ASCII DXF'e dönüştürür."""
    converter = _oda_file_converter_bul(converter_path)
    if converter is None:
        raise RuntimeError(
            "ODA File Converter bulunamadı. Bilgisayara ODA File Converter kurun veya aşağıdaki alandan ODAFileConverter.exe yolunu seçin."
        )
    import tempfile
    with tempfile.TemporaryDirectory(prefix="maki_dwg_") as tmp:
        kok = Path(tmp)
        giris = kok / "input"
        cikis = kok / "output"
        giris.mkdir(); cikis.mkdir()
        guvenli_ad = Path(dosya_adi).name
        if not guvenli_ad.lower().endswith(".dwg"):
            guvenli_ad += ".dwg"
        (giris / guvenli_ad).write_bytes(dosya_bytes)
        komut = [
            str(converter), str(giris), str(cikis),
            "ACAD2018", "DXF", "0", "1", "*.dwg"
        ]
        sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=240)
        dxfler = sorted(cikis.rglob("*.dxf"))
        if sonuc.returncode != 0 or not dxfler:
            ayrinti = (sonuc.stderr or sonuc.stdout or "Dönüştürücü çıktı üretmedi.").strip()
            raise RuntimeError(f"DWG→DXF dönüşümü başarısız: {ayrinti[:600]}")
        dxf = dxfler[0]
        return {
            "name": f"{Path(dosya_adi).stem}_AUTO.dxf",
            "bytes": dxf.read_bytes(),
            "type": "application/dxf",
            "size": int(dxf.stat().st_size),
            "source_format": "DWG",
            "source_name": dosya_adi,
            "converter": str(converter),
        }


def _topografya_yuklemesini_hesap_kaydina_cevir(uploaded_file, converter_path=""):
    """Yüklenen topoğrafya dosyasını hesapta kullanılabilir oturum kaydına çevirir."""
    ext = Path(uploaded_file.name).suffix.lower()
    if ext == ".dwg":
        try:
            return _dwg_bytes_dxf_donustur(uploaded_file.name, uploaded_file.getvalue(), converter_path)
        except Exception as hata:
            # Dönüştürücü yoksa kullanıcıyı Micrositing akışında kilitleme.
            # DWG kaynak dosyası oturumda saklanır; topoğrafya motoru hesapta
            # mevcut otomatik DEM/SRTM geri dönüşünü kullanır.
            kayit = dosyayi_kaydet(uploaded_file)
            kayit["source_format"] = "DWG"
            kayit["source_name"] = uploaded_file.name
            kayit["conversion_status"] = "raw_dwg_fallback"
            kayit["conversion_warning"] = str(hata)
            return kayit
    if ext == ".ncz":
        raise RuntimeError("NCZ doğrudan açılamıyor. Netcad'den DWG veya DXF dışa aktarımı gerekir.")
    if ext in {".tif", ".tiff", ".csv", ".xyz", ".txt", ".dxf", ".xml", ".landxml"}:
        return dosyayi_kaydet(uploaded_file)
    raise RuntimeError(f"Desteklenmeyen topoğrafya uzantısı: {ext or 'yok'}")

def _halihazir_kaynak_noktalarini_oku(kayit):
    """Oturumda saklanan halihazır dosyayı yeniden okuyup X-Y-Z noktaları döndürür."""
    if not kayit:
        return None, None
    ad = str(kayit.get("name", "")).lower()
    veri = kayit.get("bytes", b"")
    if not veri:
        return None, None
    if ad.endswith((".csv", ".txt", ".xyz")):
        return _topografya_csv_xyz_oku(veri, ad), "Nokta kotları"
    if ad.endswith((".xml", ".landxml")):
        return _topografya_landxml_oku(veri), "LandXML/TIN noktaları"
    if ad.endswith(".dxf"):
        noktalar, _ = _topografya_dxf_oku(veri)
        return noktalar, "DXF 3B kot verisi"
    return None, None


def _idw_nokta_ornekle(noktalar, hedef_x, hedef_y, komsu=12):
    """Hedef koordinatlarda yakın komşulu IDW kot örneklemesi yapar."""
    pts = noktalar[["X", "Y", "Z"]].replace([np.inf, -np.inf], np.nan).dropna().to_numpy(dtype=float)
    if len(pts) < 3:
        return np.full(len(hedef_x), np.nan, dtype=float)
    qx = np.asarray(hedef_x, dtype=float)
    qy = np.asarray(hedef_y, dtype=float)
    sonuc = np.full(len(qx), np.nan, dtype=float)
    try:
        from scipy.spatial import cKDTree
        agac = cKDTree(pts[:, :2])
        k = min(max(int(komsu), 3), len(pts))
        d, idx = agac.query(np.c_[qx, qy], k=k)
        if k == 1:
            d = d[:, None]
            idx = idx[:, None]
        w = 1.0 / np.maximum(d, 0.05) ** 2
        sonuc = np.sum(w * pts[idx, 2], axis=1) / np.sum(w, axis=1)
        tam = d[:, 0] <= 0.05
        sonuc[tam] = pts[idx[tam, 0], 2]
        return sonuc
    except Exception:
        # SciPy yoksa bellek dostu parça parça yakın komşu hesabı.
        k = min(max(int(komsu), 3), len(pts))
        for bas in range(0, len(qx), 120):
            son = min(bas + 120, len(qx))
            dx = qx[bas:son, None] - pts[None, :, 0]
            dy = qy[bas:son, None] - pts[None, :, 1]
            d2 = dx * dx + dy * dy
            idx = np.argpartition(d2, kth=k-1, axis=1)[:, :k]
            sec = np.take_along_axis(d2, idx, axis=1)
            w = 1.0 / np.maximum(sec, 0.0025)
            z = pts[idx, 2]
            vals = np.sum(w * z, axis=1) / np.sum(w, axis=1)
            tam = np.min(sec, axis=1) <= 0.0025
            if tam.any():
                nearest = idx[np.arange(len(idx)), np.argmin(sec, axis=1)]
                vals[tam] = pts[nearest[tam], 2]
            sonuc[bas:son] = vals
        return sonuc


def _halihazir_dem_gridini_ornekle(grid_lon, grid_lat, topo_kaydi, topo_crs):
    """Yüklenen GeoTIFF/DXF/LandXML/XYZ halihazır verisini WGS84 gridine örnekler.

    Dönüş değeri: (kot matrisi, kapsama maskesi, açıklama). Halihazırın kapsamadığı
    hücreler NaN bırakılır; çağıran fonksiyon bu hücreleri SRTM ile tamamlayabilir.
    """
    if not topo_kaydi:
        return None, None, "Halihazır harita yüklenmedi"
    ad = str(topo_kaydi.get("name", ""))
    ad_kucuk = ad.lower()
    veri = topo_kaydi.get("bytes", b"")
    if not veri:
        return None, None, "Halihazır dosya içeriği bulunamadı"

    lon2, lat2 = np.meshgrid(np.asarray(grid_lon, dtype=float), np.asarray(grid_lat, dtype=float))
    lon_flat = lon2.ravel()
    lat_flat = lat2.ravel()

    if ad_kucuk.endswith((".tif", ".tiff")):
        try:
            import rasterio
            from rasterio.io import MemoryFile
            from rasterio.warp import transform
        except Exception as hata:
            raise RuntimeError("GeoTIFF entegrasyonu için rasterio paketi gereklidir.") from hata
        with MemoryFile(veri) as mem:
            with mem.open() as src:
                if src.crs is None:
                    raise ValueError("GeoTIFF koordinat sistemi tanımlı değil.")
                xs, ys = transform("EPSG:4326", src.crs, lon_flat.tolist(), lat_flat.tolist())
                ornekler = list(src.sample(list(zip(xs, ys)), indexes=1, masked=True))
                vals = np.full(len(ornekler), np.nan, dtype=float)
                for i, ornek in enumerate(ornekler):
                    try:
                        deger = ornek[0]
                        if np.ma.is_masked(deger):
                            continue
                        deger = float(deger)
                        if src.nodata is not None and np.isclose(deger, float(src.nodata)):
                            continue
                        if np.isfinite(deger):
                            vals[i] = deger
                    except Exception:
                        continue
                mat = vals.reshape(lon2.shape)
                return mat, np.isfinite(mat), f"Halihazır GeoTIFF DEM · {src.crs}"

    noktalar, kaynak_adi = _halihazir_kaynak_noktalarini_oku(topo_kaydi)
    if noktalar is None:
        return None, None, f"{Path(ad).suffix.upper() or 'Dosya'} doğrudan kot hesabına uygun değil"
    if not str(topo_crs or "").strip():
        raise ValueError("Halihazır nokta/CAD verisi için koordinat sistemi veya EPSG girilmelidir.")
    try:
        from pyproj import CRS, Transformer
        kaynak_crs = CRS.from_user_input(str(topo_crs).strip())
        donusturucu = Transformer.from_crs("EPSG:4326", kaynak_crs, always_xy=True)
        hedef_x, hedef_y = donusturucu.transform(lon_flat, lat_flat)
    except Exception as hata:
        raise ValueError(f"Halihazır koordinat sistemi dönüştürülemedi: {topo_crs}") from hata

    pts = noktalar[["X", "Y", "Z"]].replace([np.inf, -np.inf], np.nan).dropna()
    xmin, xmax = float(pts["X"].min()), float(pts["X"].max())
    ymin, ymax = float(pts["Y"].min()), float(pts["Y"].max())
    # Sadece gerçek veri zarfı içindeki hücreleri halihazır kapsamı kabul et.
    kapsama = (
        (np.asarray(hedef_x) >= xmin) & (np.asarray(hedef_x) <= xmax) &
        (np.asarray(hedef_y) >= ymin) & (np.asarray(hedef_y) <= ymax)
    )
    vals = np.full(len(lon_flat), np.nan, dtype=float)
    if kapsama.any():
        vals[kapsama] = _idw_nokta_ornekle(
            pts, np.asarray(hedef_x)[kapsama], np.asarray(hedef_y)[kapsama], komsu=12
        )
    mat = vals.reshape(lon2.shape)
    return mat, np.isfinite(mat), f"Halihazır {kaynak_adi} · {topo_crs}"


# ============================================================
# TÜRBİN KÜTÜPHANESİ VE ENERJİ HESABI
# ============================================================

# Güç eğrileri kullanıcı tarafından sağlanan üretici tablolarından alınmıştır.
# Nordex eğrileri 1.20 kg/m³ hava yoğunluğu içindir. Envision eğrisi dokümanda
# "site air density" olarak verilmiştir. Goldwind tablosunda yoğunluk bilgisi yer almamaktadır.
TURBIN_KUTUPHANESI = {
    "Envision": {
        "EN-182-8.0": {
            "nominal_guc_kw": 8000,
            "rotor_capi_m": 182,
            "hub_yukseklikleri_m": [100, 110, 120, 130, 140, 150, 160],
            "power_curve_kaynagi": "Kullanıcı tarafından sağlanan Envision EN-182/8.0 tablosu",
            "hava_yogunlugu": "Site air density",
            "power_curve": {
                "wind_speed": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0],
                "power_kw":   [3, 103, 253, 479, 752, 1062, 1417, 1826, 2296, 2826, 3418, 4047, 4708, 5345, 5953, 6530, 7067, 7523, 7837, 7964, 7995, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 7857, 7601, 7344, 7087, 6830, 6573, 6316, 6057, 5800, 5544]
            }
        }
    },
    "Goldwind": {
        "GWH182-8.0MW": {
            "nominal_guc_kw": 8000,
            "rotor_capi_m": 182,
            "hub_yukseklikleri_m": [100, 110, 120, 130, 140, 150, 160],
            "power_curve_kaynagi": "Kullanıcı tarafından sağlanan Goldwind GWH182-8.0MW tablosu",
            "hava_yogunlugu": "Belirtilmemiş",
            "power_curve": {
                "wind_speed": [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0],
                "power_kw":   [6.8, 80.5, 171.7, 286.8, 461.1, 668.6, 921.0, 1217.8, 1564.4, 1962.3, 2416.1, 2921.5, 3473.7, 4053.6, 4631.7, 5187.2, 5690.3, 6162.8, 6610.4, 7033.5, 7418.8, 7719.3, 7902.1, 7980.9, 8000.0, 8000.0, 8000.0, 8000.0, 8000.0, 8000.0, 8000.0, 8000.0, 8000.0, 7979.9, 7876.4, 7665.2, 7340.7, 6975.5, 6585.3, 6185.1, 5778.2, 5407.2, 5097.9, 4827.2]
            }
        }
    },
    "Nordex": {
        "Nordex N175/6.X": {
            "nominal_guc_kw": 7000,
            "rotor_capi_m": 175,
            "hub_yukseklikleri_m": [112, 119, 135, 142, 159, 162],
            "power_curve_kaynagi": "Kullanıcı tarafından sağlanan Nordex N175/6.X tablosu",
            "hava_yogunlugu": "1.20 kg/m³",
            "power_curve": {
                "wind_speed": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0],
                "power_kw":   [71, 190, 352, 554, 797, 1086, 1428, 1829, 2295, 2831, 3440, 4091, 4744, 5378, 5939, 6354, 6645, 6838, 6951, 6998, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 6990, 6906, 6746, 6548, 6351, 6154, 5957, 5760, 5562, 5358, 5161, 4964, 4760, 4563, 4359, 4162, 3958, 3754, 3550, 3352]
            }
        },
        "Nordex N163/6.X": {
            "nominal_guc_kw": 7000,
            "rotor_capi_m": 163,
            "hub_yukseklikleri_m": [118, 138, 148, 159, 164],
            "power_curve_kaynagi": "Kullanıcı tarafından sağlanan Nordex N163/6.X tablosu",
            "hava_yogunlugu": "1.20 kg/m³",
            "power_curve": {
                "wind_speed": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0],
                "power_kw":   [42, 145, 283, 454, 659, 901, 1189, 1526, 1919, 2370, 2883, 3452, 4044, 4632, 5199, 5726, 6156, 6474, 6703, 6859, 6953, 6994, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000, 6882, 6603, 6331, 6059, 5794, 5528, 5270, 5012, 4760, 4508, 4264, 4019, 3774]
            }
        }
    }
}

KAYIP_SENARYOLARI = {
    "P50": {"wake": 8.0, "kullanilabilirlik": 3.0, "elektrik": 2.0, "diger": 2.0},
    "P75": {"wake": 10.0, "kullanilabilirlik": 4.0, "elektrik": 2.5, "diger": 3.0},
    "P90": {"wake": 12.0, "kullanilabilirlik": 5.0, "elektrik": 3.0, "diger": 4.0}
}

def saha_alpha_hesapla(veri, sensor_yukseklikleri=(0.0, 0.0, 0.0, 0.0)):
    sensor_sirasi = ["WS4_Avg", "WS3_Avg", "WS2_Avg", "WS1_Avg"]
    gelen = list(sensor_yukseklikleri or ())
    if len(gelen) < len(RUZGAR_KOLONLARI):
        gelen += [0.0] * (len(RUZGAR_KOLONLARI) - len(gelen))
    yuk_map = {k: float(gelen[i] or 0.0) for i, k in enumerate(RUZGAR_KOLONLARI)}
    kullanilan_sensorler = [
        k for k in sensor_sirasi
        if np.isfinite(yuk_map.get(k, 0.0)) and yuk_map.get(k, 0.0) > 0 and k in veri.columns
    ]
    if len(kullanilan_sensorler) < 2:
        return 0.14, 0

    eszamanli = veri[kullanilan_sensorler].replace([np.inf, -np.inf], np.nan).dropna()
    if eszamanli.empty:
        return 0.14, 0
    ortalamalar = eszamanli[kullanilan_sensorler].mean().to_numpy(dtype=float)
    yukseklikler = np.array([yuk_map[k] for k in kullanilan_sensorler], dtype=float)
    gecerli = (
        np.isfinite(ortalamalar) & (ortalamalar > 0)
        & np.isfinite(yukseklikler) & (yukseklikler > 0)
    )
    # Aynı yükseklik iki kez geldiyse regresyon tekil olur; tekilleştir.
    x = np.log(yukseklikler[gecerli])
    y = np.log(ortalamalar[gecerli])
    if len(x) < 2 or len(np.unique(np.round(x, 10))) < 2:
        return 0.14, len(eszamanli)
    try:
        alpha, _ = np.polyfit(x, y, 1)
    except (np.linalg.LinAlgError, ValueError, FloatingPointError):
        return 0.14, len(eszamanli)
    if not np.isfinite(alpha):
        alpha = 0.14
    return float(alpha), len(eszamanli)

def hedef_yukseklik_ortalama_hizi_hesapla(veri, yukseklik_haritasi, hedef_yukseklik):
    """Hedef yükseklikte ortalama rüzgar hızını güvenli biçimde hesaplar.

    Yöntem:
    - En az iki geçerli ve farklı yükseklikte WS sensörü gerekir.
    - Bütün kullanılan sensörlerin aynı anda geçerli olduğu kayıtlar esas alınır.
    - Hedef bir sensör yüksekliğiyle çakışıyorsa o sensörün eşzamanlı ortalaması döner.
    - Hedef ölçüm aralığındaysa komşu iki seviye arasında log(H)-log(V)
      doğrusal enterpolasyon (yerel power-law) uygulanır.
    - Hedef ölçüm aralığı dışındaysa tüm seviyelere log-log en küçük kareler
      power-law regresyonu uygulanarak ekstrapolasyon yapılır.
    """
    try:
        hedef = float(hedef_yukseklik)
    except (TypeError, ValueError):
        return {"ok": False, "mesaj": "Hedef yükseklik sayısal olmalıdır."}
    if not np.isfinite(hedef) or hedef <= 0:
        return {"ok": False, "mesaj": "Hedef yükseklik 0 metreden büyük olmalıdır."}

    sensorler = []
    for kolon in RUZGAR_KOLONLARI:
        try:
            h = float((yukseklik_haritasi or {}).get(kolon, 0.0) or 0.0)
        except (TypeError, ValueError):
            h = 0.0
        if kolon in veri.columns and np.isfinite(h) and h > 0:
            sensorler.append((h, kolon))

    # Aynı yükseklikte birden fazla sensör varsa ayrı kolonları koru; fakat
    # regresyon öncesi aynı yükseklikteki ortalamaları tek değerde birleştir.
    if len(sensorler) < 2:
        return {"ok": False, "mesaj": "Hesap için en az iki geçerli WS sensör yüksekliği gerekir."}

    kolonlar = [k for _, k in sensorler]
    eszamanli = veri[kolonlar].apply(pd.to_numeric, errors="coerce")
    eszamanli = eszamanli.replace([np.inf, -np.inf], np.nan)
    for kolon in kolonlar:
        eszamanli.loc[(eszamanli[kolon] <= 0) | (eszamanli[kolon] > 45), kolon] = np.nan
    eszamanli = eszamanli.dropna(subset=kolonlar)
    if eszamanli.empty:
        return {"ok": False, "mesaj": "Sensörlerin eşzamanlı geçerli kaydı bulunamadı."}

    ham_noktalar = []
    for h, kolon in sensorler:
        ort = float(eszamanli[kolon].mean())
        if np.isfinite(ort) and ort > 0:
            ham_noktalar.append((h, ort, kolon))
    if len(ham_noktalar) < 2:
        return {"ok": False, "mesaj": "Geçerli sensör ortalaması yetersiz."}

    # Aynı yükseklikler tek noktaya indirgenir.
    gruplanmis = {}
    for h, v, kolon in ham_noktalar:
        gruplanmis.setdefault(round(h, 6), []).append((v, kolon))
    noktalar = []
    for h_key, degerler in gruplanmis.items():
        noktalar.append((float(h_key), float(np.mean([v for v, _ in degerler]))))
    noktalar.sort(key=lambda x: x[0])
    if len(noktalar) < 2:
        return {"ok": False, "mesaj": "Farklı yükseklikte en az iki sensör gerekir."}

    hs = np.array([p[0] for p in noktalar], dtype=float)
    vs = np.array([p[1] for p in noktalar], dtype=float)

    # Tam sensör yüksekliği: model yerine gerçek eşzamanlı ortalamayı döndür.
    esit = np.where(np.isclose(hs, hedef, rtol=0.0, atol=1e-6))[0]
    if len(esit):
        idx = int(esit[0])
        return {
            "ok": True, "hiz": float(vs[idx]), "yontem": "Ölçülen sensör ortalaması",
            "tur": "ölçüm", "alpha": None, "r2": None,
            "kayit": int(len(eszamanli)), "alt_h": float(hs[idx]), "ust_h": float(hs[idx])
        }

    # Ölçüm aralığı içinde: iki komşu seviyede yerel power-law enterpolasyonu.
    if hs.min() < hedef < hs.max():
        ust_idx = int(np.searchsorted(hs, hedef, side="right"))
        alt_idx = ust_idx - 1
        h1, h2 = float(hs[alt_idx]), float(hs[ust_idx])
        v1, v2 = float(vs[alt_idx]), float(vs[ust_idx])
        alpha_local = float(np.log(v2 / v1) / np.log(h2 / h1))
        hiz = float(v1 * (hedef / h1) ** alpha_local)
        return {
            "ok": True, "hiz": hiz, "yontem": "Komşu sensörler arası log-log enterpolasyon",
            "tur": "enterpolasyon", "alpha": alpha_local, "r2": 1.0,
            "kayit": int(len(eszamanli)), "alt_h": h1, "ust_h": h2
        }

    # Ölçüm aralığı dışında: tüm sensör seviyelerine global power-law regresyonu.
    x = np.log(hs)
    y = np.log(vs)
    try:
        alpha, ln_a = np.polyfit(x, y, 1)
    except (np.linalg.LinAlgError, ValueError, FloatingPointError):
        return {"ok": False, "mesaj": "Power-law regresyonu hesaplanamadı."}
    if not np.isfinite(alpha) or not np.isfinite(ln_a):
        return {"ok": False, "mesaj": "Power-law regresyonu geçersiz sonuç verdi."}
    y_hat = ln_a + alpha * x
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 if ss_tot <= 1e-15 else float(1.0 - ss_res / ss_tot)
    hiz = float(np.exp(ln_a) * hedef ** alpha)
    if not np.isfinite(hiz) or hiz <= 0 or hiz > 45:
        return {"ok": False, "mesaj": "Hesaplanan hedef hız fiziksel sınırlar dışında kaldı."}
    return {
        "ok": True, "hiz": hiz, "yontem": "Tüm sensörlerle power-law ekstrapolasyonu",
        "tur": "ekstrapolasyon", "alpha": float(alpha), "r2": r2,
        "kayit": int(len(eszamanli)), "alt_h": float(hs.min()), "ust_h": float(hs.max())
    }


def zaman_adimi_saat(timestamp):
    farklar = timestamp.sort_values().diff().dt.total_seconds().dropna() / 3600.0
    farklar = farklar[(farklar > 0) & (farklar <= 6)]
    return float(farklar.median()) if not farklar.empty else (10.0 / 60.0)


def coklu_direk_hub_serisi_hazirla(veri_setleri, sensor_yukseklikleri, hub_yuksekligi):
    """Seçili direkleri kendi geçerli sensör yüksekliğiyle hub seviyesine taşır."""
    hub_serileri = []
    kullanilan_direkler = []
    alpha_bilgileri = {}

    try:
        hub_yuksekligi = float(hub_yuksekligi)
    except (TypeError, ValueError):
        return pd.DataFrame(columns=["TIMESTAMP", "Hub Rüzgar Hızı"]), [], {}
    if not np.isfinite(hub_yuksekligi) or hub_yuksekligi <= 0:
        return pd.DataFrame(columns=["TIMESTAMP", "Hub Rüzgar Hızı"]), [], {}

    for dosya_adi, veri in veri_setleri.items():
        if veri is None or veri.empty:
            continue

        yukseklikler = sensor_yukseklikleri.get(dosya_adi, {}) or {}
        # Rapordan gelen ve gerçekten veri kolonu bulunan en yüksek geçerli WS sensörünü seç.
        adaylar = []
        for kolon in ("WS1_Avg", "WS2_Avg", "WS3_Avg", "WS4_Avg"):
            try:
                yuk = float(yukseklikler.get(kolon, 0.0) or 0.0)
            except (TypeError, ValueError):
                yuk = 0.0
            if kolon in veri.columns and np.isfinite(yuk) and yuk > 0:
                adaylar.append((yuk, kolon))
        if not adaylar:
            # Yüksekliği bilinmeyen direk üretim hesabına alınmaz; sıfıra bölme yapılmaz.
            continue
        ref_yukseklik, ref_kolon = max(adaylar, key=lambda x: x[0])

        yuk_tuple = sensor_yukseklik_tuple(yukseklikler)
        if not enerji_verisi_hesaplanabilir(veri, dosya_adi, yukseklikler):
            return pd.DataFrame(columns=["TIMESTAMP", "Hub Rüzgar Hızı"]), [], {}
        temiz = olcum_kalite_verisi(veri, dosya_adi)
        alpha, alpha_kayit = enerji_shear_hesapla(temiz, yukseklikler)
        if ref_kolon not in temiz.columns:
            continue

        seri = temiz[["TIMESTAMP", ref_kolon]].copy()
        seri = seri.dropna(subset=["TIMESTAMP", ref_kolon])
        seri = seri[(seri[ref_kolon] >= 0) & (seri[ref_kolon] <= 45)]
        if seri.empty:
            continue

        oran = hub_yuksekligi / ref_yukseklik
        if not np.isfinite(oran) or oran <= 0:
            continue
        if oran != 1.0 and not np.isfinite(alpha):
            # Ölçümle hesaplanamayan shear yerine sessizce 0,14 kullanılmaz.
            return pd.DataFrame(columns=["TIMESTAMP", "Hub Rüzgar Hızı"]), [], {}
        if oran == 1.0 and not np.isfinite(alpha):
            alpha = 0.0  # Ölçüm seviyesinde yüksekliğe taşıma yapılmaz.
        seri[dosya_adi] = seri[ref_kolon] * (oran ** float(alpha))
        hub_serileri.append(seri[["TIMESTAMP", dosya_adi]])
        kullanilan_direkler.append(dosya_adi)
        alpha_bilgileri[dosya_adi] = {
            "alpha": float(alpha), "kayit": int(alpha_kayit),
            "referans_sensor": ref_kolon, "referans_yukseklik": float(ref_yukseklik),
        }

    if not hub_serileri:
        return pd.DataFrame(columns=["TIMESTAMP", "Hub Rüzgar Hızı"]), [], {}

    birlesik = hub_serileri[0]
    for seri in hub_serileri[1:]:
        birlesik = birlesik.merge(seri, on="TIMESTAMP", how="outer")

    birlesik = birlesik.sort_values("TIMESTAMP")
    birlesik["Hub Rüzgar Hızı"] = birlesik[kullanilan_direkler].mean(axis=1, skipna=True)
    birlesik = birlesik.dropna(subset=["Hub Rüzgar Hızı"])
    # Zaman adımı dışlanan kayıtlardan sonra büyütülmez; ham zaman ekseninden alınır.
    birlesik.attrs["measurement_interval_hours"] = float(np.median([
        olcum_zaman_kontrolu(veri_setleri[ad])["step_seconds"] / 3600 for ad in kullanilan_direkler]))
    return birlesik, kullanilan_direkler, alpha_bilgileri


def turbin_uretimi_coklu_direk_hesapla(
    veri_setleri, sensor_yukseklikleri, model_bilgisi, hub_yuksekligi,
    turbin_sayisi, kayiplar
):
    """Seçili direklerin hub hızlarını zaman bazında ortalayıp ortak AEP hesaplar."""
    hub, kullanilan_direkler, alpha_bilgileri = coklu_direk_hub_serisi_hazirla(
        veri_setleri, sensor_yukseklikleri, hub_yuksekligi
    )
    if hub.empty:
        return None

    hesap = hub[["TIMESTAMP", "Hub Rüzgar Hızı"]].copy()
    curve = model_bilgisi["power_curve"]
    hesap["Tek Türbin Güç kW"] = np.interp(
        hesap["Hub Rüzgar Hızı"].to_numpy(),
        np.asarray(curve["wind_speed"], dtype=float),
        np.asarray(curve["power_kw"], dtype=float),
        left=0.0, right=0.0
    )
    dt_saat = float(hub.attrs["measurement_interval_hours"])
    hesap["Santral Brüt Güç kW"] = hesap["Tek Türbin Güç kW"] * int(turbin_sayisi)
    hesap["Tek Türbin Enerji kWh"] = hesap["Tek Türbin Güç kW"] * dt_saat
    hesap["Santral Brüt Enerji kWh"] = hesap["Santral Brüt Güç kW"] * dt_saat

    net_carpan = 1.0
    for oran in kayiplar.values():
        net_carpan *= (1.0 - float(oran) / 100.0)
    hesap["Santral Net Güç kW"] = hesap["Santral Brüt Güç kW"] * net_carpan
    hesap["Santral Net Enerji kWh"] = hesap["Santral Net Güç kW"] * dt_saat

    brut_mwh = hesap["Santral Brüt Enerji kWh"].sum() / 1000.0
    net_mwh = hesap["Santral Net Enerji kWh"].sum() / 1000.0
    sure_saat = len(hesap) * dt_saat
    kurulu_guc_mw = model_bilgisi["nominal_guc_kw"] * int(turbin_sayisi) / 1000.0
    ort_guc_mw = net_mwh / sure_saat if sure_saat > 0 else 0.0
    quality = {ad:enerji_kalite_durumu(veri_setleri[ad],ad,sensor_yukseklikleri[ad])[3] for ad in kullanilan_direkler}
    annual_ok = all(q["annual_ok"] for q in quality.values())
    # Takvim aylarını kendi uzunluklarına göre ağırlıklandır; eksik mevsimi kalan kayıtla kapatma.
    month_power = hesap.groupby(hesap["TIMESTAMP"].dt.month)["Santral Net Güç kW"].mean()
    month_days = pd.Series({1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31})
    yillik_net_mwh = float((month_power.reindex(range(1,13))*month_days*24).sum()/1000) if annual_ok and month_power.size==12 else np.nan
    kapasite_faktoru = (yillik_net_mwh/(kurulu_guc_mw*8760)*100) if np.isfinite(yillik_net_mwh) and kurulu_guc_mw>0 else np.nan

    return {
        "quality":quality,"annual_ok":bool(np.isfinite(yillik_net_mwh)),
        "hesap": hesap, "alpha": np.nan, "alpha_kayit": len(hesap),
        "dt_saat": dt_saat, "brut_mwh": brut_mwh, "net_mwh": net_mwh,
        "yillik_net_mwh": yillik_net_mwh, "kurulu_guc_mw": kurulu_guc_mw,
        "kapasite_faktoru": kapasite_faktoru, "net_carpan": net_carpan,
        "kullanilan_direkler": kullanilan_direkler,
        "alpha_bilgileri": alpha_bilgileri,
        "metod": "Seçili direklerin hub seviyesindeki eşzamanlı ortalaması"
    }

@st.cache_data(show_spinner=False, max_entries=24)
def turbin_uretimi_hesapla(temiz_veri, model_bilgisi, hub_yuksekligi, turbin_sayisi, kayiplar, sensor_yukseklikleri=(0.0, 0.0, 0.0, 0.0)):
    # Geriye dönük tek-direk hesabı; en yüksek geçerli sensörü güvenli biçimde seçer.
    gelen = list(sensor_yukseklikleri or ())
    if len(gelen) < len(RUZGAR_KOLONLARI):
        gelen += [0.0] * (len(RUZGAR_KOLONLARI) - len(gelen))
    adaylar = []
    for i, kolon in enumerate(RUZGAR_KOLONLARI):
        try:
            yuk = float(gelen[i] or 0.0)
        except (TypeError, ValueError):
            yuk = 0.0
        if kolon in temiz_veri.columns and np.isfinite(yuk) and yuk > 0:
            adaylar.append((yuk, kolon))
    if not adaylar:
        return None
    ref_yukseklik, ref_kolon = max(adaylar, key=lambda x: x[0])
    hesap = temiz_veri[["TIMESTAMP", ref_kolon]].copy()
    hesap = hesap.dropna(subset=["TIMESTAMP", ref_kolon])
    hesap = hesap[(hesap[ref_kolon] >= 0) & (hesap[ref_kolon] <= 45)]
    if hesap.empty:
        return None
    alpha, alpha_kayit = saha_alpha_hesapla(temiz_veri, tuple(gelen[:4]))
    oran = float(hub_yuksekligi) / float(ref_yukseklik)
    if not np.isfinite(oran) or oran <= 0:
        return None
    hesap["Hub Rüzgar Hızı"] = hesap[ref_kolon] * (oran ** alpha)

    curve = model_bilgisi["power_curve"]
    hesap["Tek Türbin Güç kW"] = np.interp(
        hesap["Hub Rüzgar Hızı"].to_numpy(),
        np.asarray(curve["wind_speed"], dtype=float),
        np.asarray(curve["power_kw"], dtype=float), left=0.0, right=0.0
    )
    dt_saat = zaman_adimi_saat(hesap["TIMESTAMP"])
    hesap["Santral Brüt Güç kW"] = hesap["Tek Türbin Güç kW"] * int(turbin_sayisi)
    hesap["Tek Türbin Enerji kWh"] = hesap["Tek Türbin Güç kW"] * dt_saat
    hesap["Santral Brüt Enerji kWh"] = hesap["Santral Brüt Güç kW"] * dt_saat
    net_carpan = 1.0
    for oran_kayip in kayiplar.values():
        net_carpan *= (1.0 - float(oran_kayip) / 100.0)
    hesap["Santral Net Güç kW"] = hesap["Santral Brüt Güç kW"] * net_carpan
    hesap["Santral Net Enerji kWh"] = hesap["Santral Net Güç kW"] * dt_saat
    brut_mwh = hesap["Santral Brüt Enerji kWh"].sum() / 1000.0
    net_mwh = hesap["Santral Net Enerji kWh"].sum() / 1000.0
    sure_saat = len(hesap) * dt_saat
    kurulu_guc_mw = model_bilgisi["nominal_guc_kw"] * int(turbin_sayisi) / 1000.0
    ort_guc_mw = net_mwh / sure_saat if sure_saat > 0 else 0.0
    yillik_net_mwh = np.nan  # Bu eski yordam bağımsız veri kapsamı onayı olmadan yıllıklaştırmaz.
    kapasite_faktoru = np.nan
    return {
        "hesap": hesap, "alpha": alpha, "alpha_kayit": alpha_kayit,
        "dt_saat": dt_saat, "brut_mwh": brut_mwh, "net_mwh": net_mwh,
        "yillik_net_mwh": yillik_net_mwh, "kurulu_guc_mw": kurulu_guc_mw,
        "kapasite_faktoru": kapasite_faktoru, "net_carpan": net_carpan,
        "referans_sensor": ref_kolon, "referans_yukseklik": ref_yukseklik,
    }


def _koordinat_metnini_noktalara_cevir(koordinat_metni):
    """KML coordinates metnini kapalı (lon, lat) poligonuna çevirir."""
    noktalar = []
    if not koordinat_metni:
        return noktalar

    for parca in koordinat_metni.replace("\n", " ").replace("\t", " ").split():
        degerler = [d.strip() for d in parca.split(",")]
        if len(degerler) < 2:
            continue
        try:
            lon = float(degerler[0])
            lat = float(degerler[1])
        except (TypeError, ValueError):
            continue
        if np.isfinite(lon) and np.isfinite(lat):
            noktalar.append((lon, lat))

    # Ardışık aynı noktaları temizle.
    temiz = []
    for nokta in noktalar:
        if not temiz or nokta != temiz[-1]:
            temiz.append(nokta)

    if len(temiz) >= 3 and temiz[0] != temiz[-1]:
        temiz.append(temiz[0])
    return temiz


def _kml_kmz_kaynaklarini_oku(yuklenen_dosya):
    """KML dosyasını veya KMZ içindeki bütün KML dosyalarını bytes olarak döndürür."""
    if yuklenen_dosya is None:
        return []

    dosya_adi = yuklenen_dosya.name.lower()
    dosya_bytes = yuklenen_dosya.getvalue()

    if dosya_adi.endswith(".kml"):
        return [(yuklenen_dosya.name, dosya_bytes)]

    if not dosya_adi.endswith(".kmz"):
        raise ValueError("Yalnızca KML veya KMZ dosyası yükleyin.")

    try:
        with zipfile.ZipFile(io.BytesIO(dosya_bytes), "r") as kmz:
            kml_adlari = sorted(
                ad for ad in kmz.namelist()
                if ad.lower().endswith(".kml") and not ad.endswith("/")
            )
            if not kml_adlari:
                raise ValueError("KMZ dosyasının içinde KML bulunamadı.")
            return [(ad, kmz.read(ad)) for ad in kml_adlari]
    except zipfile.BadZipFile as hata:
        raise ValueError("KMZ dosyası açılamadı veya bozuk.") from hata


def _kml_bytes_poligonlarini_oku(kml_bytes):
    """Bir KML içindeki Polygon dış ve iç halkalarını güvenli biçimde okur."""
    try:
        root = ET.fromstring(kml_bytes)
    except ET.ParseError as hata:
        raise ValueError(f"KML okunamadı: {hata}") from hata

    dis_poligonlar = []
    ic_poligonlar = []

    # Namespace bağımsız çalışmak için etiketlerin son bölümünü kullan.
    for polygon in root.iter():
        if polygon.tag.split("}")[-1] != "Polygon":
            continue

        for sinir in polygon.iter():
            yerel_ad = sinir.tag.split("}")[-1]
            if yerel_ad not in {"outerBoundaryIs", "innerBoundaryIs"}:
                continue

            for eleman in sinir.iter():
                if eleman.tag.split("}")[-1] != "coordinates":
                    continue
                noktalar = _koordinat_metnini_noktalara_cevir(eleman.text)
                if len(noktalar) >= 4:
                    if yerel_ad == "outerBoundaryIs":
                        dis_poligonlar.append(noktalar)
                    else:
                        ic_poligonlar.append(noktalar)

    # Bazı hatalı/alışılmadık KML'lerde Polygon düğümü olmayabilir.
    # Bu durumda yalnızca en az 3 noktalı kapalı koordinat dizilerini yedek olarak al.
    if not dis_poligonlar:
        for eleman in root.iter():
            if eleman.tag.split("}")[-1] == "coordinates" and eleman.text:
                noktalar = _koordinat_metnini_noktalara_cevir(eleman.text)
                if len(noktalar) >= 4:
                    dis_poligonlar.append(noktalar)

    return dis_poligonlar, ic_poligonlar


def _poligon_alani_yaklasik(poligon):
    """Sadece en büyük dış sınırı seçmek için shoelace alanı hesaplar."""
    if len(poligon) < 4:
        return 0.0
    x = np.asarray([p[0] for p in poligon], dtype=float)
    y = np.asarray([p[1] for p in poligon], dtype=float)
    return float(abs(np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])) / 2.0)


def kml_kmz_sinirlarini_oku(yuklenen_dosya):
    """
    KML/KMZ içindeki bütün KML dosyalarını ve bütün Polygon geometrilerini tarar.
    Ana santral sınırı olarak alanı en büyük outerBoundary poligonunu döndürür.
    """
    tum_dis_poligonlar = []
    hatalar = []

    for kaynak_adi, kml_bytes in _kml_kmz_kaynaklarini_oku(yuklenen_dosya):
        try:
            dis_poligonlar, _ = _kml_bytes_poligonlarini_oku(kml_bytes)
            tum_dis_poligonlar.extend(dis_poligonlar)
        except ValueError as hata:
            hatalar.append(f"{kaynak_adi}: {hata}")

    if not tum_dis_poligonlar:
        ayrinti = " | ".join(hatalar[:3])
        mesaj = "KMZ/KML içinde geçerli Polygon dış sınırı bulunamadı."
        if ayrinti:
            mesaj += f" Ayrıntı: {ayrinti}"
        raise ValueError(mesaj)

    return max(tum_dis_poligonlar, key=_poligon_alani_yaklasik)


def nokta_poligon_icinde(lon, lat, poligon):
    """Ray casting yöntemiyle noktanın poligon içinde olup olmadığını kontrol eder."""
    icerde = False
    j = len(poligon) - 1
    for i in range(len(poligon)):
        xi, yi = poligon[i]
        xj, yj = poligon[j]
        kesiyor = ((yi > lat) != (yj > lat)) and (
            lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi
        )
        if kesiyor:
            icerde = not icerde
        j = i
    return icerde


def _yukseklikleri_otomatik_getir(noktalar, parti_boyutu=50, zaman_asimi=30, tekrar_sayisi=4):
    """OpenTopoData SRTM90m servisinden kot getirir.

    429/rate-limit durumunda Retry-After ve artan bekleme uygular. Nokta
    sonuçları disk önbelleğinde tutulur; aynı saha için servis tekrar çağrılmaz.
    """
    if not noktalar:
        return []

    cache_dir = Path.home() / ".maki_wind_studio" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "opentopodata_srtm90_cache.json"
    try:
        disk_cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    except Exception:
        disk_cache = {}

    def anahtar(lon, lat):
        return f"{float(lon):.5f},{float(lat):.5f}"

    sonuclar = [np.nan] * len(noktalar)
    eksik_indeksler = []
    for i, (lon, lat) in enumerate(noktalar):
        k = anahtar(lon, lat)
        if k in disk_cache:
            try:
                sonuclar[i] = float(disk_cache[k])
                continue
            except Exception:
                pass
        eksik_indeksler.append(i)

    for baslangic in range(0, len(eksik_indeksler), max(1, int(parti_boyutu))):
        idx_parti = eksik_indeksler[baslangic:baslangic + max(1, int(parti_boyutu))]
        parti = [noktalar[i] for i in idx_parti]
        locations = "|".join(f"{lat:.6f},{lon:.6f}" for lon, lat in parti)
        veri = urllib.parse.urlencode({
            "locations": locations,
            "interpolation": "bilinear",
            "nodata_value": "null",
        }).encode("utf-8")

        son_hata = None
        payload = None
        for deneme in range(max(1, int(tekrar_sayisi))):
            istek = urllib.request.Request(
                "https://api.opentopodata.org/v1/srtm90m",
                data=veri,
                headers={"User-Agent": "Maki-Wind-Studio/11.6.3"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(istek, timeout=float(zaman_asimi)) as cevap:
                    payload = json.loads(cevap.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as hata:
                son_hata = hata
                if int(getattr(hata, "code", 0)) != 429 or deneme >= int(tekrar_sayisi) - 1:
                    raise
                retry_after = hata.headers.get("Retry-After") if getattr(hata, "headers", None) else None
                try:
                    bekle = float(retry_after)
                except Exception:
                    bekle = [3.0, 8.0, 18.0, 30.0][min(deneme, 3)]
                time.sleep(max(1.0, min(bekle, 35.0)))
            except Exception as hata:
                son_hata = hata
                if deneme >= int(tekrar_sayisi) - 1:
                    raise
                time.sleep([2.0, 5.0, 10.0, 20.0][min(deneme, 3)])

        if payload is None:
            raise RuntimeError(f"Kot servisi yanıt vermedi: {son_hata}")
        if payload.get("status") != "OK":
            raise RuntimeError(payload.get("error") or "Kot servisi geçerli yanıt vermedi.")
        parcali = payload.get("results") or []
        if len(parcali) != len(parti):
            raise RuntimeError("Kot servisinden eksik nokta döndü.")
        for hedef_i, (lon, lat), kayit in zip(idx_parti, parti, parcali):
            deger = kayit.get("elevation")
            if deger is not None:
                val = float(deger)
                sonuclar[hedef_i] = val
                disk_cache[anahtar(lon, lat)] = val
        try:
            gecici = cache_file.with_suffix(".tmp")
            gecici.write_text(json.dumps(disk_cache), encoding="utf-8")
            gecici.replace(cache_file)
        except Exception:
            pass
        if baslangic + int(parti_boyutu) < len(eksik_indeksler):
            time.sleep(0.8)
    return sonuclar


@st.cache_data(show_spinner=False, ttl=24 * 3600)
def _yukseklikleri_otomatik_getir_cache(noktalar_tuple):
    return _yukseklikleri_otomatik_getir(list(noktalar_tuple))


def _komsu_ortalama(matris, tekrar=2):
    """SciPy gerektirmeden 3x3 yumuşatma uygular; DEM gürültüsünü azaltır."""
    sonuc = np.asarray(matris, dtype=float).copy()
    for _ in range(max(int(tekrar), 0)):
        p = np.pad(sonuc, 1, mode="edge")
        toplam = (
            p[:-2, :-2] + 2*p[:-2, 1:-1] + p[:-2, 2:] +
            2*p[1:-1, :-2] + 4*p[1:-1, 1:-1] + 2*p[1:-1, 2:] +
            p[2:, :-2] + 2*p[2:, 1:-1] + p[2:, 2:]
        )
        sonuc = toplam / 16.0
    return sonuc


def _bilinear_matris_degeri(matris, satir, sutun):
    """Ondalıklı grid indeksinde güvenli bilinear örnekleme."""
    n_satir, n_sutun = matris.shape
    satir = float(np.clip(satir, 0.0, n_satir - 1.0))
    sutun = float(np.clip(sutun, 0.0, n_sutun - 1.0))
    r0, c0 = int(np.floor(satir)), int(np.floor(sutun))
    r1, c1 = min(r0 + 1, n_satir - 1), min(c0 + 1, n_sutun - 1)
    fr, fc = satir - r0, sutun - c0
    return float(
        matris[r0, c0] * (1-fr) * (1-fc) +
        matris[r1, c0] * fr * (1-fc) +
        matris[r0, c1] * (1-fr) * fc +
        matris[r1, c1] * fr * fc
    )


def _gaussian_yumusat(matris, sigma_hucre=1.2):
    """SciPy gerektirmeyen ayrilabilir Gaussian yumuşatma."""
    a = np.asarray(matris, dtype=float)
    sigma = max(float(sigma_hucre), 0.35)
    yaricap = max(1, int(np.ceil(3.0 * sigma)))
    x = np.arange(-yaricap, yaricap + 1, dtype=float)
    kernel = np.exp(-0.5 * (x / sigma) ** 2)
    kernel /= kernel.sum()
    p = np.pad(a, ((0, 0), (yaricap, yaricap)), mode="edge")
    yatay = np.empty_like(a)
    for r in range(a.shape[0]):
        yatay[r] = np.convolve(p[r], kernel, mode="valid")
    p = np.pad(yatay, ((yaricap, yaricap), (0, 0)), mode="edge")
    dikey = np.empty_like(a)
    for c in range(a.shape[1]):
        dikey[:, c] = np.convolve(p[:, c], kernel, mode="valid")
    return dikey


def _matris_kaydir_bilinear(matris, dr, dc):
    """Bir matrisi kesirli hücre kadar bilinear kaydırır."""
    a = np.asarray(matris, dtype=float)
    nr, nc = a.shape
    rr = np.arange(nr, dtype=float)[:, None] + float(dr)
    cc = np.arange(nc, dtype=float)[None, :] + float(dc)
    rr = np.clip(rr, 0.0, nr - 1.0)
    cc = np.clip(cc, 0.0, nc - 1.0)
    r0 = np.floor(rr).astype(int); c0 = np.floor(cc).astype(int)
    r1 = np.minimum(r0 + 1, nr - 1); c1 = np.minimum(c0 + 1, nc - 1)
    fr = rr - r0; fc = cc - c0
    return (
        a[r0, c0] * (1-fr) * (1-fc) +
        a[r1, c0] * fr * (1-fc) +
        a[r0, c1] * (1-fr) * fc +
        a[r1, c1] * fr * fc
    )


def _sektor_agirliklari(hakim_yon_deg, sektor_sayisi=12, konsantrasyon=2.8):
    """Hakim yön çevresinde von-Mises benzeri 12 sektör ağırlığı üretir."""
    sektor_sayisi = max(int(sektor_sayisi), 4)
    yonler = np.linspace(0.0, 360.0, sektor_sayisi, endpoint=False)
    fark = np.radians(((yonler - float(hakim_yon_deg) + 180.0) % 360.0) - 180.0)
    w = np.exp(float(konsantrasyon) * np.cos(fark))
    w = w / np.sum(w)
    return yonler, w


def _yonlu_arazi_etkisi(z_mat, dx, dy, hakim_yon_deg):
    """Çok ölçekli ve sektörel topoğrafik hızlanma/korunak modeli.

    Tek bir eğim katsayısı yerine 12 yön sektörü çözülür. Her sektörde:
    - yerel yönlü eğim,
    - çok ölçekli upwind bağıl kot,
    - sırt/vadi (TPI ve eğrilik),
    - upwind engel açısı,
    - downwind açıklık
    birlikte değerlendirilir. Sonuç hakim yön frekansına göre birleştirilir.
    """
    z0 = np.asarray(z_mat, dtype=float)
    z = _gaussian_yumusat(z0, 0.9)
    nr, nc = z.shape
    hucre_m = max((float(dx) + float(dy)) / 2.0, 1.0)

    dz_dy, dz_dx = np.gradient(z, float(dy), float(dx))
    d2z_dx2 = np.gradient(dz_dx, float(dx), axis=1)
    d2z_dy2 = np.gradient(dz_dy, float(dy), axis=0)
    lap = d2z_dx2 + d2z_dy2
    lap_scale = max(float(np.nanpercentile(np.abs(lap), 92)), 1e-7)
    ridge = np.clip(-lap / lap_scale, -2.5, 2.5)

    # Çok ölçekli TPI: dar ve geniş sırtları birlikte yakalar.
    sigma_small = max(1.0, 180.0 / hucre_m)
    sigma_mid = max(1.2, 450.0 / hucre_m)
    sigma_large = max(1.5, 1000.0 / hucre_m)
    tpi_s = z - _gaussian_yumusat(z, sigma_small)
    tpi_m = z - _gaussian_yumusat(z, sigma_mid)
    tpi_l = z - _gaussian_yumusat(z, sigma_large)
    tpi_scale = max(float(np.nanpercentile(np.abs(np.r_[tpi_s.ravel(), tpi_m.ravel(), tpi_l.ravel()]), 92)), 1.0)
    tpi = np.clip((0.50*tpi_s + 0.35*tpi_m + 0.15*tpi_l) / tpi_scale, -2.5, 2.5)

    sektor_yonleri, sektor_w = _sektor_agirliklari(hakim_yon_deg, 12, 2.8)
    log_toplam = np.zeros_like(z, dtype=float)
    yonlu_egim_toplam = np.zeros_like(z, dtype=float)
    engel_toplam = np.zeros_like(z, dtype=float)

    mesafeler_m = np.array([120, 240, 400, 650, 950, 1400, 2000, 2800], dtype=float)
    mesafe_w = np.array([0.05, 0.08, 0.12, 0.16, 0.18, 0.17, 0.14, 0.10], dtype=float)
    mesafe_w /= mesafe_w.sum()

    for sektor_deg, sw in zip(sektor_yonleri, sektor_w):
        theta = np.radians(float(sektor_deg))
        # Meteorolojik yön geliş yönüdür; akış ters yöndedir.
        akis_x = -np.sin(theta)
        akis_y = -np.cos(theta)
        yonlu_egim = dz_dx * akis_x + dz_dy * akis_y
        capraz_egim = -dz_dx * akis_y + dz_dy * akis_x

        up_rel = np.zeros_like(z)
        down_rel = np.zeros_like(z)
        max_obstacle = np.full_like(z, -np.inf)
        max_opening = np.full_like(z, -np.inf)

        for mesafe, mw in zip(mesafeler_m, mesafe_w):
            step = mesafe / hucre_m
            # Upwind: akış vektörünün tersi, downwind: akış yönü.
            up = _matris_kaydir_bilinear(z, -akis_y*step, -akis_x*step)
            down = _matris_kaydir_bilinear(z, akis_y*step, akis_x*step)
            up_rel += mw * (z - up) / max(mesafe, 1.0)
            down_rel += mw * (z - down) / max(mesafe, 1.0)
            max_obstacle = np.maximum(max_obstacle, np.arctan2(up - z, mesafe))
            max_opening = np.maximum(max_opening, np.arctan2(z - down, mesafe))

        slope_term = np.clip(yonlu_egim, -0.28, 0.28)
        up_term = np.clip(up_rel, -0.20, 0.20)
        down_term = np.clip(down_rel, -0.20, 0.20)
        obstacle = np.clip(np.maximum(max_obstacle, 0.0), 0.0, 0.30)
        opening = np.clip(np.maximum(max_opening, 0.0), 0.0, 0.22)
        cross_penalty = np.clip(np.abs(capraz_egim), 0.0, 0.30)

        # Kalibre edilmiş ön-mühendislik log hız çarpanı.
        sector_log = (
            0.90*slope_term +
            1.65*up_term +
            0.12*tpi +
            0.055*ridge -
            1.10*obstacle +
            0.38*opening +
            0.45*np.maximum(down_term, 0.0) -
            0.10*cross_penalty
        )
        sector_log = np.clip(sector_log, np.log(0.76), np.log(1.28))
        log_toplam += float(sw) * sector_log
        yonlu_egim_toplam += float(sw) * yonlu_egim
        engel_toplam += float(sw) * np.degrees(max_obstacle)

    # Yüzeyi noktasal benek yerine sürekli raster haline getir.
    log_toplam = _gaussian_yumusat(log_toplam, 1.0)
    carpan = np.exp(np.clip(log_toplam, np.log(0.78), np.log(1.24)))
    return {
        "carpan": carpan,
        "yonlu_egim": yonlu_egim_toplam,
        "engel_acisi_deg": engel_toplam,
        "sirtlik": 0.55*tpi + 0.45*ridge,
        "sektor_sayisi": len(sektor_yonleri),
    }




# ESA WorldCover 2021 v200 arazi ortusu siniflari -> aerodinamik puruzluluk uzunlugu (z0, metre).
# Degerler on muhendislik icin muhafazakar temsil degerleridir; ekranda acikca gosterilir.
WORLDCOVER_Z0 = {
    10: ("Agac ortusu", 1.00),
    20: ("Calilik", 0.30),
    30: ("Cayir", 0.03),
    40: ("Tarim alani", 0.10),
    50: ("Yapilasmis alan", 1.00),
    60: ("Ciplak / seyrek bitkili", 0.01),
    70: ("Kar ve buz", 0.003),
    80: ("Kalici su", 0.0002),
    90: ("Otsu sulak alan", 0.05),
    95: ("Mangrov", 0.80),
    100: ("Yosun / liken", 0.10),
}

def _worldcover_tile_kodu(lat, lon):
    """ESA WorldCover 3x3 derece COG karo adini hesaplar."""
    import math
    lat0 = int(math.floor(float(lat) / 3.0) * 3)
    lon0 = int(math.floor(float(lon) / 3.0) * 3)
    ns = "N" if lat0 >= 0 else "S"
    ew = "E" if lon0 >= 0 else "W"
    return f"{ns}{abs(lat0):02d}{ew}{abs(lon0):03d}", lat0, lon0

def _worldcover_cache_dir():
    klasor = Path.home() / ".maki_wind_studio" / "cache" / "worldcover_2021_v200"
    klasor.mkdir(parents=True, exist_ok=True)
    return klasor

def _worldcover_tile_indir(tile_kodu, zaman_asimi=90):
    """WorldCover COG karosunu resmi acik AWS bucketindan indirip onbellege alir."""
    dosya_adi = f"ESA_WorldCover_10m_2021_v200_{tile_kodu}_Map.tif"
    hedef = _worldcover_cache_dir() / dosya_adi
    if hedef.exists() and hedef.stat().st_size > 100000:
        return hedef
    url = f"https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/{dosya_adi}"
    gecici = hedef.with_suffix('.part')
    istek = urllib.request.Request(url, headers={"User-Agent": "Maki-Wind-Studio/11.5"})
    try:
        with urllib.request.urlopen(istek, timeout=float(zaman_asimi)) as cevap, open(gecici, 'wb') as cikti:
            while True:
                parca = cevap.read(1024 * 1024)
                if not parca:
                    break
                cikti.write(parca)
        if gecici.stat().st_size < 100000:
            raise RuntimeError("WorldCover karosu beklenenden kucuk indi.")
        gecici.replace(hedef)
        return hedef
    except Exception:
        try:
            gecici.unlink(missing_ok=True)
        except Exception:
            pass
        raise

@st.cache_data(show_spinner=False, ttl=7 * 24 * 3600)
def _worldcover_ornekle_cache(noktalar_tuple):
    """Lon/lat noktalarinda WorldCover siniflarini ornekler. rasterio yoksa acik hata verir."""
    try:
        import rasterio
    except Exception as hata:
        raise RuntimeError("ESA WorldCover analizi icin 'rasterio' paketi kurulu degil.") from hata
    noktalar = list(noktalar_tuple)
    sonuc = np.full(len(noktalar), np.nan, dtype=float)
    karo_gruplari = {}
    for idx, (lon, lat) in enumerate(noktalar):
        kod, _, _ = _worldcover_tile_kodu(lat, lon)
        karo_gruplari.setdefault(kod, []).append((idx, float(lon), float(lat)))
    for kod, grup in karo_gruplari.items():
        yol = _worldcover_tile_indir(kod)
        with rasterio.open(yol) as kaynak:
            coords = [(lon, lat) for _, lon, lat in grup]
            ornekler = list(kaynak.sample(coords, indexes=1))
            for (idx, _, _), deger in zip(grup, ornekler):
                try:
                    sonuc[idx] = float(deger[0])
                except Exception:
                    sonuc[idx] = np.nan
    return sonuc.tolist()

def _worldcover_z0_matrisi(sinif_mat):
    z0 = np.full(np.asarray(sinif_mat).shape, np.nan, dtype=float)
    for kod, (_, deger) in WORLDCOVER_Z0.items():
        z0[np.asarray(sinif_mat) == kod] = float(deger)
    return z0

def _yonlu_etkin_puruzluluk(z0_mat, dx, dy, hakim_yon_deg):
    """Hakim ruzgarin geldigi yone dogru 0-1500 m fetch boyunca log-agirlikli etkin z0 hesaplar."""
    z0 = np.asarray(z0_mat, dtype=float)
    gecerli = np.isfinite(z0) & (z0 > 0)
    varsayilan = float(np.nanmedian(z0[gecerli])) if gecerli.any() else 0.05
    z0 = np.where(gecerli, z0, varsayilan)
    theta = np.radians(float(hakim_yon_deg) % 360.0)
    up_x = np.sin(theta)
    up_y = np.cos(theta)
    mesafeler = np.array([0, 150, 350, 700, 1100, 1500], dtype=float)
    agirliklar = np.array([0.28, 0.22, 0.18, 0.14, 0.10, 0.08], dtype=float)
    log_toplam = np.zeros_like(z0, dtype=float)
    for mesafe, agirlik in zip(mesafeler, agirliklar):
        dr = up_y * mesafe / max(float(dy), 1.0)
        dc = up_x * mesafe / max(float(dx), 1.0)
        ornek = np.empty_like(z0, dtype=float)
        for r in range(z0.shape[0]):
            for c in range(z0.shape[1]):
                ornek[r, c] = _bilinear_matris_degeri(z0, r + dr, c + dc)
        log_toplam += float(agirlik) * np.log(np.clip(ornek, 0.0001, 3.0))
    return np.exp(log_toplam / agirliklar.sum())

def _puruzluluk_hiz_carpani(etkin_z0, referans_z0, hub_yuksekligi):
    h = max(float(hub_yuksekligi), 20.0)
    ref = float(np.clip(referans_z0, 0.0001, min(3.0, h / 5.0)))
    z = np.clip(np.asarray(etkin_z0, dtype=float), 0.0001, min(3.0, h / 5.0))
    pay = np.log(h / z)
    payda = max(np.log(h / ref), 0.2)
    return np.clip(pay / payda, 0.88, 1.12)





def _gwa_cache_dir():
    klasor = Path.home() / ".maki_wind_studio" / "cache" / "global_wind_atlas"
    klasor.mkdir(parents=True, exist_ok=True)
    return klasor


def _gwa_iso2_iso3(iso2):
    iso2 = str(iso2 or "").strip().upper()
    if not iso2:
        return None
    # Projenin ana kullanım alanı için bağımsız fallback.
    sabit = {
        "TR": "TUR", "GR": "GRC", "BG": "BGR", "RO": "ROU", "GE": "GEO",
        "AZ": "AZE", "AM": "ARM", "CY": "CYP", "GB": "GBR", "DE": "DEU",
        "FR": "FRA", "ES": "ESP", "IT": "ITA", "PT": "PRT", "NL": "NLD",
        "BE": "BEL", "DK": "DNK", "SE": "SWE", "NO": "NOR", "FI": "FIN",
        "PL": "POL", "UA": "UKR", "US": "USA", "CA": "CAN", "AU": "AUS",
    }
    if iso2 in sabit:
        return sabit[iso2]
    try:
        import pycountry
        ulke = pycountry.countries.get(alpha_2=iso2)
        if ulke:
            return str(ulke.alpha_3).upper()
    except Exception:
        pass
    # pycountry yoksa ücretsiz REST Countries dönüşümü yalnız son çare olarak kullanılır.
    try:
        req = urllib.request.Request(
            f"https://restcountries.com/v3.1/alpha/{urllib.parse.quote(iso2)}?fields=cca3",
            headers={"User-Agent": "Maki-Wind-Studio/11.7.2"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        if isinstance(payload, dict) and payload.get("cca3"):
            return str(payload["cca3"]).upper()
    except Exception:
        pass
    return None


def _gwa_ulke_iso3_otomatik(poligon):
    """Çalışma poligonu merkezinden GWA country API için ISO-3166 alpha-3 kodu bulur."""
    if not poligon:
        raise ValueError("GWA ülke tespiti için çalışma poligonu bulunamadı.")
    lon = float(np.mean([p[0] for p in poligon]))
    lat = float(np.mean([p[1] for p in poligon]))

    # Türkiye için ağ servisinden bağımsız güvenli kısa yol. Bu kutu komşu ülkeleri
    # kapsayabildiğinden yalnız Trakya/Anadolu genel sınırları içinde ilk fallback'tir.
    if 25.5 <= lon <= 45.0 and 35.5 <= lat <= 42.5:
        # Çorlu gibi mevcut Maki sahalarında kesin TUR sonucu sağlar. Sınır bölgelerinde
        # Nominatim varsa aşağıdaki doğrulama yine kullanılabilir; erişilemiyorsa TUR kalır.
        tur_fallback = "TUR"
    else:
        tur_fallback = None

    try:
        params = urllib.parse.urlencode({
            "format": "jsonv2", "lat": f"{lat:.7f}", "lon": f"{lon:.7f}",
            "zoom": 3, "addressdetails": 1,
        })
        req = urllib.request.Request(
            "https://nominatim.openstreetmap.org/reverse?" + params,
            headers={
                "User-Agent": "Maki-Wind-Studio/11.7.2 (GWA country detection)",
                "Accept-Language": "en",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        iso2 = ((payload.get("address") or {}).get("country_code") or "").upper()
        iso3 = _gwa_iso2_iso3(iso2)
        if iso3:
            return iso3, str((payload.get("address") or {}).get("country") or iso3)
    except Exception:
        pass

    if tur_fallback:
        return tur_fallback, "Türkiye"
    raise RuntimeError(
        "GWA için ülke otomatik belirlenemedi. İnternet bağlantısını kontrol edin. "
        "Türkiye projelerinde bu adım ağ olmadan da TUR olarak çalışır."
    )


def _gwa_json_url_adaylari(nesne):
    """GWA API JSON yanıtındaki olası indirme URL'lerini derinlemesine bulur."""
    adaylar = []
    if isinstance(nesne, dict):
        # Önce semantik olarak olası anahtarları tercih et.
        oncelikli = (
            "url", "href", "download", "downloadUrl", "download_url", "file",
            "fileUrl", "file_url", "tif", "tiff", "geotiff", "data", "result"
        )
        for anahtar in oncelikli:
            if anahtar in nesne:
                adaylar.extend(_gwa_json_url_adaylari(nesne[anahtar]))
        for anahtar, deger in nesne.items():
            if anahtar not in oncelikli:
                adaylar.extend(_gwa_json_url_adaylari(deger))
    elif isinstance(nesne, (list, tuple)):
        for deger in nesne:
            adaylar.extend(_gwa_json_url_adaylari(deger))
    elif isinstance(nesne, str):
        metin = nesne.strip().strip('"\'')
        if metin.lower().startswith(("http://", "https://")):
            adaylar.append(metin)
    # Sıra koruyarak tekilleştir.
    sonuc = []
    goruldu = set()
    for url in adaylar:
        if url not in goruldu:
            goruldu.add(url)
            sonuc.append(url)
    return sonuc


def _gwa_indirilen_rasteri_ayikla(data):
    """GWA yanıtından GeoTIFF bytes çıkarır.

    GWA'nın GIS endpoint'i sürüme göre ham TIFF, ZIP/GZIP, JSON içinde geçici
    indirme URL'si veya düz metin URL döndürebilir. Bu fonksiyon yalnız binary
    katmanları ayıklar; URL takip işi `_gwa_http_raster_getir` tarafından yapılır.
    """
    if not data or len(data) < 8:
        raise RuntimeError("GWA API boş veya çok küçük veri döndürdü.")
    # TIFF little/big endian imzaları.
    if data[:4] in (b"II*\x00", b"MM\x00*"):
        return data
    # BigTIFF imzaları.
    if data[:4] in (b"II+\x00", b"MM\x00+"):
        return data
    if data[:2] == b"PK":
        try:
            with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
                adaylar = [n for n in zf.namelist() if n.lower().endswith((".tif", ".tiff"))]
                if not adaylar:
                    raise RuntimeError("GWA ZIP yanıtında GeoTIFF bulunamadı.")
                aday = max(adaylar, key=lambda n: zf.getinfo(n).file_size)
                return zf.read(aday)
        except zipfile.BadZipFile as hata:
            raise RuntimeError("GWA API ZIP yanıtı bozuk.") from hata
    if data[:2] == b"\x1f\x8b":
        try:
            return _gwa_indirilen_rasteri_ayikla(gzip.decompress(data))
        except Exception as hata:
            raise RuntimeError("GWA GZIP yanıtı açılamadı.") from hata
    raise RuntimeError("GWA yanıtı doğrudan GeoTIFF/ZIP/GZIP değil.")


def _gwa_http_raster_getir(url, timeout=240, max_takip=5):
    """GWA GIS endpoint'ini çağırır ve gerekirse JSON/metin içindeki indirme URL'sini takip eder."""
    mevcut = str(url).strip()
    ziyaret = set()
    son_ozet = ""
    for _ in range(max(1, int(max_takip))):
        if mevcut in ziyaret:
            raise RuntimeError("GWA indirme yönlendirmesi döngüye girdi.")
        ziyaret.add(mevcut)
        req = urllib.request.Request(
            mevcut,
            headers={
                "User-Agent": "Maki-Wind-Studio/11.7.2",
                "Accept": "application/octet-stream,application/zip,image/tiff,application/json,text/plain,*/*",
                "Referer": "https://globalwindatlas.info/",
            },
        )
        with urllib.request.urlopen(req, timeout=float(timeout)) as resp:
            ham = resp.read()
            ctype = str(resp.headers.get("Content-Type") or "").lower()
            final_url = str(getattr(resp, "url", mevcut) or mevcut)
            disposition = str(resp.headers.get("Content-Disposition") or "")
        son_ozet = f"content-type={ctype or 'yok'}, boyut={len(ham)}, final={final_url}"

        # Önce binary veri olarak dene.
        try:
            return _gwa_indirilen_rasteri_ayikla(ham), final_url
        except RuntimeError:
            pass

        # JSON yanıt: signed/download URL bul ve takip et.
        metin = ham.decode("utf-8", errors="ignore").strip()
        json_nesne = None
        if "json" in ctype or (metin.startswith("{") or metin.startswith("[")):
            try:
                json_nesne = json.loads(metin)
            except Exception:
                json_nesne = None
        if json_nesne is not None:
            adaylar = _gwa_json_url_adaylari(json_nesne)
            if adaylar:
                mevcut = urllib.parse.urljoin(final_url, adaylar[0])
                continue

        # Düz metin URL yanıtı.
        temiz = metin.strip().strip('"\'')
        if temiz.lower().startswith(("http://", "https://")) and "\n" not in temiz:
            mevcut = temiz
            continue

        # HTML/XML içinde olası .tif/.zip/signed URL bağlantısı.
        url_eslesmeleri = re.findall(r'https?://[^\s"\'<>]+', metin, flags=re.I)
        tercih = [u for u in url_eslesmeleri if any(x in u.lower() for x in (".tif", ".tiff", ".zip", "download", "storage", "blob"))]
        if tercih:
            mevcut = tercih[0].replace("&amp;", "&")
            continue

        ilk = re.sub(r"\s+", " ", metin[:220])
        raise RuntimeError(
            "GWA GIS API geçerli raster veya indirilebilir URL döndürmedi. "
            f"{son_ozet}. Yanıt başlangıcı: {ilk!r}"
        )
    raise RuntimeError(f"GWA indirme URL'si {max_takip} yönlendirme içinde rastera ulaşmadı. {son_ozet}")


def _gwa_otomatik_country_raster_getir(poligon, gwa_yukseklik_m=100, timeout=240):
    iso3, ulke_adi = _gwa_ulke_iso3_otomatik(poligon)
    h = int(gwa_yukseklik_m)
    if h not in {10, 50, 100, 150, 200}:
        raise ValueError("GWA Mean Wind Speed yüksekliği 10, 50, 100, 150 veya 200 m olmalıdır.")
    cache = _gwa_cache_dir() / f"GWA4_{iso3}_wind-speed_{h}m.tif"
    if cache.exists() and cache.stat().st_size > 1024:
        try:
            # Cache gerçekten raster mı; bozuk eski JSON/cache dosyasını kullanma.
            eski = cache.read_bytes()
            _gwa_indirilen_rasteri_ayikla(eski)
            return eski, f"Global Wind Atlas API · {ulke_adi} ({iso3}) · {h} m · disk cache", "auto-api", iso3
        except Exception:
            try:
                cache.unlink()
            except Exception:
                pass

    # GWA'nın resmi ve belgelenmiş ülke GIS endpoint'i.
    url = f"https://globalwindatlas.info/api/gis/country/{iso3}/wind-speed/{h}"
    try:
        tif, final_url = _gwa_http_raster_getir(url, timeout=timeout, max_takip=6)
        gecici = cache.with_suffix(".part")
        gecici.write_bytes(tif)
        gecici.replace(cache)
        return tif, f"Global Wind Atlas API · {ulke_adi} ({iso3}) · {h} m", "auto-api", iso3
    except urllib.error.HTTPError as hata:
        raise RuntimeError(f"GWA resmi GIS API HTTP {hata.code}: {hata.reason} · {url}") from hata
    except Exception as hata:
        raise RuntimeError(f"GWA resmi GIS API verisi otomatik indirilemedi: {hata}") from hata


def _gwa_raster_bytes_getir(tif_kaydi=None, api_url="", poligon=None,
                             gwa_yukseklik_m=100, timeout=240):
    """GWA rasterını otomatik getirir; manuel TIF/URL yalnız isteğe bağlı override'dır."""
    if tif_kaydi and tif_kaydi.get("bytes"):
        tif = _gwa_indirilen_rasteri_ayikla(tif_kaydi["bytes"])
        return tif, f"GWA GeoTIFF · {tif_kaydi.get('name','Mean Wind Speed')}", "upload", None
    url = str(api_url or "").strip()
    if url:
        if not url.lower().startswith(("https://", "http://")):
            raise ValueError("GWA API/GIS URL'si http:// veya https:// ile başlamalıdır.")
        try:
            tif, final_url = _gwa_http_raster_getir(url, timeout=timeout, max_takip=6)
            return tif, f"GWA GIS/API · {final_url}", "url", None
        except urllib.error.HTTPError as hata:
            raise RuntimeError(f"GWA GIS/API HTTP {hata.code}: {hata.reason}") from hata
        except Exception as hata:
            raise RuntimeError(f"GWA GIS/API verisi indirilemedi: {hata}") from hata
    return _gwa_otomatik_country_raster_getir(poligon, gwa_yukseklik_m, timeout)

def _gwa_geotiff_ornekle(tif_bytes, lonlar, latlar):
    """GWA GeoTIFF örnekleme: rasterio gerekmeden tifffile kullanır.

    Desteklenen georeferanslar: north-up ModelPixelScale + ModelTiepoint,
    veya ModelTransformation. Desteklenmeyen CRS/transform açık hata verir.
    """
    try:
        import tifffile
    except Exception as exc:
        raise RuntimeError("GWA GeoTIFF için saf Python TIFF okuyucusu eksik: pip install tifffile") from exc
    import io
    lonlar = np.asarray(lonlar, dtype=float)
    latlar = np.asarray(latlar, dtype=float)
    if lonlar.shape != latlar.shape:
        raise ValueError("GWA örnekleme koordinatları uyumsuz.")
    # TIFF Predictor=3 (floating-point) decoder without imagecodecs native DLL.
    # This is for single-band GWA float32/float64 rasters.
    def _gwa_float_predictor_decode(data, axis=-2, out=None):
        import sys
        a = np.asarray(data)
        if a.dtype.kind != "f" or a.dtype.itemsize not in (4, 8):
            raise ValueError("GWA float predictor supports float32/float64 only")
        # tifffile uses (..., rows, columns, samples), axis=-2.
        axis = axis % a.ndim
        if a.shape[-1] != 1:
            raise ValueError("GWA floating-point predictor: only single-band raster supported")
        moved = np.moveaxis(a, axis, -2)
        ncol = moved.shape[-2]
        nbytes = a.dtype.itemsize
        b = np.ascontiguousarray(moved).view(np.uint8).reshape(-1, ncol * nbytes)
        planes = b.reshape(-1, nbytes, ncol).copy()
        # Undo horizontal byte differencing, independently for each byte plane.
        planes = np.cumsum(planes, axis=2, dtype=np.uint32).astype(np.uint8)
        # Undo byte-plane shuffle; predictor stores most-significant bytes first.
        if sys.byteorder == "little":
            planes = planes[:, ::-1, :]
        restored = planes.transpose(0, 2, 1).copy().reshape(-1).view(a.dtype).reshape(moved.shape)
        result = np.moveaxis(restored, -2, axis)
        if out is not None:
            # tifffile may supply a read-only buffer (e.g. bytes-backed data).
            # Never write into it: return the newly decoded writable array.
            target = np.asarray(out)
            if target.flags.writeable and target.shape == result.shape:
                target[...] = result
                return out
        return np.array(result, copy=True)

    # Native imagecodecs DLLs can be blocked by Windows Smart App Control.
    # Register Python stdlib codecs before tifffile resolves any native decoder.
    import zlib
    import lzma
    tifffile.TIFF.UNPREDICTORS._codecs[3] = _gwa_float_predictor_decode
    def _gwa_zlib_decode(data, out=None, **kwargs):
        return zlib.decompress(data)
    def _gwa_lzma_decode(data, out=None, **kwargs):
        return lzma.decompress(data)
    for compression in (8, 32946, 50013):
        tifffile.TIFF.DECOMPRESSORS._codecs[compression] = _gwa_zlib_decode
    tifffile.TIFF.DECOMPRESSORS._codecs[34925] = _gwa_lzma_decode
    with tifffile.TiffFile(io.BytesIO(tif_bytes)) as tif:
        page = tif.pages[0]
        tags = page.tags
        def tag_value(code):
            tag = tags.get(code)
            return None if tag is None else tag.value
        keys = tag_value(34735)
        epsg = None
        if keys is not None:
            keys = list(keys)
            for i in range(int(keys[3])):
                offset = 4 + i * 4
                key_id, location, count, value = keys[offset:offset+4]
                if key_id in (3072, 2048) and location == 0 and count == 1 and value not in (0, 32767):
                    epsg = int(value)
                    break
        if epsg is None:
            raise ValueError("GWA GeoTIFF EPSG kodu bulunamadı; yanlış koordinatla harita çizilmeyecek.")
        crs = f"EPSG:{epsg}"
        xs, ys = lonlar, latlar
        if epsg == 3857:
            # EPSG:3857 Web Mercator, analytic WGS84 conversion; no pyproj DLL.
            clipped_lat = np.clip(latlar, -85.05112878, 85.05112878)
            xs = 6378137.0 * np.deg2rad(lonlar)
            ys = 6378137.0 * np.log(np.tan(np.pi / 4.0 + np.deg2rad(clipped_lat) / 2.0))
        elif epsg != 4326:
            raise RuntimeError(
                f"GWA raster CRS {crs} için güvenli dönüşüm bulunamadı. "
                "EPSG:4326 veya EPSG:3857 GeoTIFF kullanın."
            )
        matrix = tag_value(34264)
        if matrix is not None:
            m = np.asarray(matrix, dtype=float).reshape(4, 4)
            affine = m[:2, :2]
            if abs(np.linalg.det(affine)) < 1e-15:
                raise ValueError("GeoTIFF dönüşüm matrisi tekil.")
            inv = np.linalg.inv(affine)
            coords = inv @ np.vstack((np.asarray(xs).ravel()-m[0,3], np.asarray(ys).ravel()-m[1,3]))
            cols, rows = coords[0], coords[1]
            def world(c, r):
                return (m[0,0]*c + m[0,1]*r + m[0,3], m[1,0]*c + m[1,1]*r + m[1,3])
        else:
            scale, tie = tag_value(33550), tag_value(33922)
            if scale is None or tie is None:
                raise ValueError("GeoTIFF koordinatlandırma etiketleri eksik.")
            sx, sy = float(scale[0]), float(scale[1])
            if sx <= 0 or sy <= 0:
                raise ValueError("GeoTIFF piksel boyutu geçersiz.")
            x0 = float(tie[3]) - float(tie[0])*sx
            y0 = float(tie[4]) + float(tie[1])*sy
            cols = (np.asarray(xs).ravel()-x0)/sx
            rows = (y0-np.asarray(ys).ravel())/sy
            def world(c, r):
                return (x0 + c*sx, y0 - r*sy)
        # Read only the first raster band; no interpolation or fabricated data.
        arr = page.asarray()
        if arr.ndim == 3:
            arr = arr[0] if arr.shape[0] == 1 else arr[..., 0]
        if arr.ndim != 2:
            raise ValueError("GWA GeoTIFF tek bantlı 2B raster değil.")
        h, w = arr.shape
        finite = np.isfinite(cols) & np.isfinite(rows)
        ix = np.floor(np.where(finite, cols, -1)).astype(np.int64)
        iy = np.floor(np.where(finite, rows, -1)).astype(np.int64)
        valid = finite & (ix >= 0) & (ix < w) & (iy >= 0) & (iy < h)
        values = np.full(lonlar.size, np.nan, dtype=float)
        values[valid] = np.asarray(arr[iy[valid], ix[valid]], dtype=float)
        nodata_tag = tag_value(42113)
        if nodata_tag is not None:
            try:
                nodata = float(str(nodata_tag).strip().strip(chr(0)))
                values[np.isclose(values, nodata)] = np.nan
            except ValueError:
                pass
        values[~(np.isfinite(values) & (values > 0) & (values < 60))] = np.nan
        corners = [world(0,0), world(w,0), world(0,h), world(w,h)]
        bounds = (min(x for x,y in corners), min(y for x,y in corners),
                  max(x for x,y in corners), max(y for x,y in corners))
        return values.reshape(lonlar.shape), crs, bounds


def _gwa_ruzg_haritasi_uret(poligon, direk_noktalari, tif_kaydi=None, api_url="",
                            gwa_yukseklik_m=100, hub_yuksekligi=100.0,
                            grid_boyutu=60, kalibre_et=True):
    """Global Wind Atlas Mean Wind Speed rasterından saha rüzgâr gridini üretir.

    GWA'nın mekânsal desenini korur. Kalibrasyon açıksa GWA değeri her ölçüm
    direğinde ölçülmüş hub-height ortalamasına oranlanır. Tek direkte sabit bir
    ölçek; çoklu direkte ise uzaklık ve veri kalitesi ağırlıklı yumuşak bir
    ölçek alanı kullanılır. Direk noktaları nihai tabloda kesin kontrol noktasıdır.
    """
    if not poligon:
        return pd.DataFrame()
    tif_bytes, kaynak, kaynak_tipi, iso3 = _gwa_raster_bytes_getir(
        tif_kaydi, api_url, poligon=poligon, gwa_yukseklik_m=gwa_yukseklik_m
    )
    n = int(np.clip(int(grid_boyutu), 24, 120))
    lon_min, lon_max = min(p[0] for p in poligon), max(p[0] for p in poligon)
    lat_min, lat_max = min(p[1] for p in poligon), max(p[1] for p in poligon)
    grid_lon = np.linspace(lon_min, lon_max, n)
    grid_lat = np.linspace(lat_min, lat_max, n)
    lon2, lat2 = np.meshgrid(grid_lon, grid_lat)
    inside = np.array([
        nokta_poligon_icinde(float(lo), float(la), poligon)
        for lo, la in zip(lon2.ravel(), lat2.ravel())
    ], dtype=bool)
    qlon = lon2.ravel()[inside]
    qlat = lat2.ravel()[inside]
    if qlon.size == 0:
        raise ValueError("Çalışma alanında GWA için örneklenecek grid noktası bulunamadı.")
    ham, crs, bounds = _gwa_geotiff_ornekle(tif_bytes, qlon, qlat)
    ham = np.array(ham, dtype=float, copy=True)
    gecerli = np.isfinite(ham) & (ham > 0)
    if gecerli.sum() < max(12, int(0.25 * len(ham))):
        raise ValueError(
            "GWA GeoTIFF çalışma alanını yeterince kapsamıyor. GWA'dan proje alanını kapsayan "
            "Mean Wind Speed TIF dosyasını indirin."
        )
    # QA: Ham rasterdaki dama-tahtasi artefaktlarini kalibrasyonla gizleme.
    # Ornekleme tam duzenli kare oldugundan komsu farklarini denetle.
    _raw_full = np.full(lon2.size, np.nan, dtype=float)
    _raw_full[inside] = ham
    _raw_full = _raw_full.reshape(lon2.shape)
    _dx = np.abs(np.diff(_raw_full, axis=1))
    _dy = np.abs(np.diff(_raw_full, axis=0))
    _neighbors = np.concatenate([_dx[np.isfinite(_dx)], _dy[np.isfinite(_dy)]])
    _center = float(np.nanmedian(ham[gecerli]))
    if _neighbors.size >= 100:
        _jump_fraction = float(np.mean(_neighbors > max(1.8, 0.25 * _center)))
        _jump_median = float(np.median(_neighbors))
        if _jump_fraction > 0.12 and _jump_median > max(0.6, 0.09 * _center):
            raise ValueError(
                "GWA veri kalite kontrolu basarisiz: bitisik raster hucrelerinde "
                f"anormal hiz sicramalari saptandi (%{100*_jump_fraction:.1f}). "
                "Bu veriyle ruzgar haritasi ve AEP hesaplanmadi. "
                "GeoTIFF predictor/cozumleme dogrulanmali."
            )
    # Kalibrasyon öncesi düzenli gridde keskin komşu sıçramalarını engelle.
    _raw_grid = np.full(lon2.size, np.nan, dtype=float)
    _raw_grid[inside] = ham
    _raw_grid = _raw_grid.reshape(lon2.shape)
    _horizontal = np.abs(np.diff(_raw_grid, axis=1))
    _vertical = np.abs(np.diff(_raw_grid, axis=0))
    _edges = np.r_[_horizontal[np.isfinite(_horizontal)], _vertical[np.isfinite(_vertical)]]
    if _edges.size >= 50:
        _typical = float(np.nanmedian(ham[gecerli]))
        _large = _edges > max(1.5, _typical * 0.20)
        if float(np.mean(_large)) > 0.08:
            raise ValueError("GWA raster kalite kontrolü: bitişik hücrelerde çok fazla ani hız değişimi var. TIFF kod çözücü doğrulanana kadar harita ve AEP hesaplanmayacak.")
    # Kenarlardaki tekil nodata hücrelerini en yakın geçerli GWA değeriyle doldur.
    if not gecerli.all():
        try:
            from scipy.spatial import cKDTree
            xy_ok = np.c_[qlon[gecerli], qlat[gecerli]]
            tree = cKDTree(xy_ok)
            _, idx = tree.query(np.c_[qlon[~gecerli], qlat[~gecerli]], k=1)
            ham[~gecerli] = ham[gecerli][idx]
        except Exception:
            ham[~gecerli] = float(np.nanmedian(ham[gecerli]))

    kal_carpan = np.ones_like(ham, dtype=float)
    kal_noktalari = []
    ileri, _ = latlon_xy_donustur(poligon)
    gx = np.array([ileri(float(lo), float(la))[0] for lo, la in zip(qlon, qlat)], dtype=float)
    gy = np.array([ileri(float(lo), float(la))[1] for lo, la in zip(qlon, qlat)], dtype=float)

    if bool(kalibre_et) and direk_noktalari:
        mlon = np.array([float(d["lon"]) for d in direk_noktalari], dtype=float)
        mlat = np.array([float(d["lat"]) for d in direk_noktalari], dtype=float)
        gwa_mast, _, _ = _gwa_geotiff_ornekle(tif_bytes, mlon, mlat)
        for d, gv in zip(direk_noktalari, gwa_mast):
            mh = float(d.get("hub_hizi", np.nan))
            if np.isfinite(gv) and gv > 0 and np.isfinite(mh) and mh > 0:
                # GWA katmanı farklı yükseklikteyse bu oran aynı zamanda hub-height düzeltmesini içerir.
                ratio = float(np.clip(mh / gv, 0.50, 2.00))
                mx, my = ileri(float(d["lon"]), float(d["lat"]))
                kal_noktalari.append((mx, my, ratio, float(d.get("agirlik", 1.0)), gv, mh, d))
        if len(kal_noktalari) == 1:
            kal_carpan[:] = kal_noktalari[0][2]
        elif len(kal_noktalari) > 1:
            # GWA bölgesel desenini koruyup mast bias'ını mekânsal ve yumuşak düzelt.
            spacing = []
            for a in range(len(kal_noktalari)):
                for b in range(a + 1, len(kal_noktalari)):
                    spacing.append(np.hypot(kal_noktalari[a][0]-kal_noktalari[b][0], kal_noktalari[a][1]-kal_noktalari[b][1]))
            L = float(np.clip(np.nanmedian(spacing) if spacing else 5000.0, 1500.0, 12000.0))
            pay = np.zeros_like(ham)
            payda = np.zeros_like(ham)
            for mx, my, ratio, kalite, *_ in kal_noktalari:
                d2 = (gx-mx)**2 + (gy-my)**2
                w = np.exp(-0.5*d2/max(L*L, 1.0)) * max(kalite, 0.05)
                pay += w * ratio
                payda += w
            kal_carpan = np.divide(pay, payda, out=np.ones_like(pay), where=payda > 1e-12)
            kal_carpan = np.clip(kal_carpan, 0.50, 2.00)

    hiz = ham * kal_carpan
    satirlar = pd.DataFrame({
        "lat": qlat.astype(float),
        "lon": qlon.astype(float),
        "Hub Rüzgar Hızı (m/s)": hiz.astype(float),
        f"GWA Ham Hız @{int(gwa_yukseklik_m)}m (m/s)": ham.astype(float),
        "GWA Kalibrasyon Çarpanı": kal_carpan.astype(float),
        "Model Güven Skoru": np.full_like(ham, np.nan, dtype=float),
        "Harita Yöntemi": (
            f"Global Wind Atlas Mean Wind Speed @{int(gwa_yukseklik_m)} m"
            + (" + ölçüm direği kalibrasyonu" if bool(kalibre_et) and kal_noktalari else "")
        ),
        "Rüzgâr Veri Kaynağı": kaynak,
        "GWA Raster CRS": crs,
        "Nokta Türü": "Raster grid",
        "Kullanılan Direk Sayısı": len(kal_noktalari),
    })
    satirlar["GWA Katman Yüksekliği (m)"] = int(gwa_yukseklik_m)
    satirlar["GWA Ülke ISO3"] = iso3 or "Manuel/URL"
    satirlar["Hedef Hub Yüksekliği (m)"] = float(hub_yuksekligi)

    if kal_noktalari:
        kontroller = []
        for mx, my, ratio, kalite, gv, mh, d in kal_noktalari:
            kontroller.append({
                "lat": float(d["lat"]), "lon": float(d["lon"]),
                "Hub Rüzgar Hızı (m/s)": float(mh),
                f"GWA Ham Hız @{int(gwa_yukseklik_m)}m (m/s)": float(gv),
                "GWA Kalibrasyon Çarpanı": float(ratio),
                "Model Güven Skoru": 1.0,
                "Harita Yöntemi": "GWA direk kalibrasyon kontrol noktası",
                "Rüzgâr Veri Kaynağı": kaynak,
                "GWA Raster CRS": crs,
                "Nokta Türü": "Direk kontrol noktası",
                "Kullanılan Direk Sayısı": len(kal_noktalari),
                "GWA Katman Yüksekliği (m)": int(gwa_yukseklik_m),
                "Hedef Hub Yüksekliği (m)": float(hub_yuksekligi),
                "Model Hatası (m/s)": 0.0,
            })
        satirlar = pd.concat([satirlar, pd.DataFrame(kontroller)], ignore_index=True, sort=False)

    grid_mask = satirlar["Nokta Türü"].eq("Raster grid")
    satirlar["Referans Saha Ortalaması (m/s)"] = float(np.average(
        [float(d["hub_hizi"]) for d in direk_noktalari],
        weights=[float(d.get("agirlik", 1.0)) for d in direk_noktalari]
    )) if direk_noktalari else np.nan
    satirlar["Grid Ortalaması (m/s)"] = float(satirlar.loc[grid_mask, "Hub Rüzgar Hızı (m/s)"].mean())
    return satirlar

# OpenFOAM/WSL CFD motoru v11.8.0 ile kaldırıldı.
# Micrositing rüzgâr alanı yalnız Global Wind Atlas üzerinden üretilir.

def ruzgar_haritasi_uret(poligon, direk_noktalari, grid_boyutu=34, idw_gucu=2.0,
                         hakim_yon_deg=0.0, otomatik_arazi=True,
                         otomatik_puruzluluk=True, hub_yuksekligi=100.0,
                         ortalama_koru=True, referans_saha_hizi=None,
                         halihazir_topografya=None, halihazir_crs=""):
    """DEM akış etkisi + direk ölçüm kalibrasyonu ile arazi duyarlı rüzgâr gridi üretir.

    Model sırası:
    1) varsa yüklenen yüksek çözünürlüklü halihazır DEM/kot verisi,
       halihazırın kapsamadığı hücrelerde SRTM90m tamamlaması,
    2) hakim yön boyunca eğim/sırt/engel/korunak çözümü,
    3) her direğin ölçümünü kendi topoğrafya çarpanından arındırma,
    4) arındırılmış bölgesel hız alanını mesafeye göre birleştirme,
    5) yerel topoğrafya çarpanını yeniden uygulama,
    6) saha grid ortalamasını ölçüm direklerinden türetilen ağırlıklı referans ortalamaya eşitleme.

    Bu sonuç ön mühendislik/micrositing haritasıdır; bankable enerji değerlendirmesinde
    WAsP, WindPRO, OpenWind veya CFD doğrulaması yine gereklidir.
    """
    if not direk_noktalari:
        return pd.DataFrame()

    gecerli = []
    for d in direk_noktalari:
        try:
            lon = float(d["lon"]); lat = float(d["lat"]); hiz = float(d["hub_hizi"])
        except (KeyError, TypeError, ValueError):
            continue
        if np.isfinite(lon) and np.isfinite(lat) and np.isfinite(hiz) and hiz > 0:
            agirlik = float(d.get("agirlik", 1.0) or 1.0)
            if not np.isfinite(agirlik) or agirlik <= 0:
                agirlik = 1.0
            gecerli.append({**d, "lon": lon, "lat": lat, "hub_hizi": hiz, "agirlik": agirlik})
    if not gecerli:
        return pd.DataFrame()

    ileri, _ = latlon_xy_donustur(poligon)
    direk_xy = []
    for d in gecerli:
        x, y = ileri(d["lon"], d["lat"])
        direk_xy.append({**d, "x": x, "y": y})

    lonlar = [p[0] for p in poligon]
    latlar = [p[1] for p in poligon]
    n = max(36, min(int(grid_boyutu), 140))
    grid_lon = np.linspace(min(lonlar), max(lonlar), n)
    grid_lat = np.linspace(min(latlar), max(latlar), n)
    tum_noktalar = [(float(lon), float(lat)) for lat in grid_lat for lon in grid_lon]

    kotlar = np.full(len(tum_noktalar), np.nan, dtype=float)
    arazi_durumu = "Kot verisi kullanılmadı"
    halihazir_mat = None
    halihazir_mask = None
    halihazir_aciklama = "Halihazır harita yüklenmedi"

    # Öncelik her zaman kullanıcının yüklediği yüksek çözünürlüklü halihazır veridedir.
    if halihazir_topografya:
        try:
            topo_listesi = halihazir_topografya if isinstance(halihazir_topografya, (list, tuple)) else [halihazir_topografya]
            birlesik = None
            aciklamalar = []
            for topo_kaydi in topo_listesi:
                if not topo_kaydi:
                    continue
                mat_i, mask_i, aciklama_i = _halihazir_dem_gridini_ornekle(
                    grid_lon, grid_lat, topo_kaydi, halihazir_crs
                )
                if mat_i is None:
                    continue
                mat_i = np.asarray(mat_i, dtype=float)
                if birlesik is None:
                    birlesik = np.full(mat_i.shape, np.nan, dtype=float)
                # Dosya sırasına göre yalnız boş hücreleri doldur; ilk yüklenen kaynak önceliklidir.
                doldur = np.isfinite(mat_i) & ~np.isfinite(birlesik)
                birlesik[doldur] = mat_i[doldur]
                aciklamalar.append(aciklama_i)
            if birlesik is not None and np.isfinite(birlesik).any():
                halihazir_mat = birlesik
                halihazir_mask = np.isfinite(birlesik)
                halihazir_aciklama = " + ".join(aciklamalar)
                kotlar = birlesik.ravel()
            else:
                halihazir_aciklama = "Yüklenen halihazır dosyalarda çalışma alanını kapsayan kot bulunamadı"
        except Exception as hata:
            halihazir_mat = None
            halihazir_mask = None
            halihazir_aciklama = f"Halihazır okunamadı ({type(hata).__name__}: {hata})"

    # Halihazırın kapsamadığı hücreleri SRTM ile tamamla; halihazır değerlerinin üstüne yazma.
    eksik_mask = ~np.isfinite(kotlar)
    srtm_kullanildi = False
    if otomatik_arazi and bool(eksik_mask.any()):
        try:
            srtm = np.asarray(_yukseklikleri_otomatik_getir_cache(tuple(tum_noktalar)), dtype=float)
            srtm_gecerli = np.isfinite(srtm)
            doldur = eksik_mask & srtm_gecerli
            kotlar[doldur] = srtm[doldur]
            srtm_kullanildi = bool(doldur.any())
        except Exception:
            srtm_kullanildi = False

    halihazir_hucre = int(np.isfinite(np.asarray(halihazir_mat)).sum()) if halihazir_mat is not None else 0
    toplam_hucre = int(len(kotlar))
    if halihazir_hucre > 0 and srtm_kullanildi:
        oran = 100.0 * halihazir_hucre / max(toplam_hucre, 1)
        arazi_durumu = f"{halihazir_aciklama} + dış alan SRTM90m tamamlaması · halihazır kapsama %{oran:.1f}"
    elif halihazir_hucre > 0:
        arazi_durumu = f"{halihazir_aciklama} · tamamen halihazır topoğrafya"
    elif np.isfinite(kotlar).sum() >= max(16, int(0.70 * len(kotlar))):
        arazi_durumu = "OpenTopoData SRTM90m + 12 sektörlü çok ölçekli arazi akış modeli"
    else:
        arazi_durumu = f"Kot verisi yetersiz; ölçüm tabanlı geri dönüş · {halihazir_aciklama}"

    z_mat = kotlar.reshape((n, n))
    arazi_var = np.isfinite(z_mat).any()
    if arazi_var:
        z_med = float(np.nanmedian(z_mat))
        z_mat = np.where(np.isfinite(z_mat), z_mat, z_med)
        x0, _ = ileri(grid_lon[0], float(np.mean(grid_lat)))
        x1, _ = ileri(grid_lon[-1], float(np.mean(grid_lat)))
        _, y0 = ileri(float(np.mean(grid_lon)), grid_lat[0])
        _, y1 = ileri(float(np.mean(grid_lon)), grid_lat[-1])
        dx = max(abs(x1 - x0) / max(n - 1, 1), 1.0)
        dy = max(abs(y1 - y0) / max(n - 1, 1), 1.0)
        topo = _yonlu_arazi_etkisi(z_mat, dx, dy, hakim_yon_deg)
        arazi_carpani = topo["carpan"]
        yonlu_egim = topo["yonlu_egim"]
        engel_acisi = topo["engel_acisi_deg"]
        sirtlik = topo["sirtlik"]
    else:
        z_mat = np.full((n, n), np.nan)
        arazi_carpani = np.ones((n, n), dtype=float)
        yonlu_egim = np.zeros((n, n), dtype=float)
        engel_acisi = np.zeros((n, n), dtype=float)
        sirtlik = np.zeros((n, n), dtype=float)

    # ESA WorldCover 10 m arazi ortusu -> yonlu etkin puruzluluk (z0) katmani.
    wc_sinif = np.full((n, n), np.nan, dtype=float)
    z0_mat = np.full((n, n), np.nan, dtype=float)
    etkin_z0 = np.full((n, n), np.nan, dtype=float)
    puruzluluk_carpani = np.ones((n, n), dtype=float)
    puruzluluk_durumu = "Puruzluluk katmani kullanilmadi"
    if otomatik_puruzluluk:
        try:
            wc_degerleri = np.asarray(_worldcover_ornekle_cache(tuple(tum_noktalar)), dtype=float)
            wc_sinif = wc_degerleri.reshape((n, n))
            z0_mat = _worldcover_z0_matrisi(wc_sinif)
            if np.isfinite(z0_mat).sum() >= max(16, int(0.70 * z0_mat.size)):
                etkin_z0 = _yonlu_etkin_puruzluluk(z0_mat, dx if arazi_var else 30.0, dy if arazi_var else 30.0, hakim_yon_deg)
                # Referans z0 once direklerin bulundugu hucrelerden, olmazsa saha medyanindan bulunur.
                mast_z0lar = []
                for d in direk_xy:
                    cc = np.interp(d["lon"], [grid_lon[0], grid_lon[-1]], [0, n-1])
                    rr = np.interp(d["lat"], [grid_lat[0], grid_lat[-1]], [0, n-1])
                    mast_z0lar.append(_bilinear_matris_degeri(etkin_z0, rr, cc))
                ref_z0 = float(np.nanmedian(mast_z0lar)) if np.isfinite(mast_z0lar).any() else float(np.nanmedian(etkin_z0))
                puruzluluk_carpani = _puruzluluk_hiz_carpani(etkin_z0, ref_z0, hub_yuksekligi)
                puruzluluk_durumu = "ESA WorldCover 2021 v200 10 m + yonlu 1.5 km etkin z0"
            else:
                puruzluluk_durumu = "WorldCover verisi yetersiz; puruzluluk etkisi uygulanmadi"
        except Exception as hata:
            puruzluluk_durumu = f"WorldCover erisilemedi; puruzluluk etkisi uygulanmadi ({type(hata).__name__})"

    toplam_yerel_carpan = np.clip(arazi_carpani * puruzluluk_carpani, 0.78, 1.22)

    # Direklerin bulunduğu hücrelerdeki topoğrafya + puruzluluk çarpanını bul ve ölçümü normalize et.
    for d in direk_xy:
        c = np.interp(d["lon"], [grid_lon[0], grid_lon[-1]], [0, n-1])
        r = np.interp(d["lat"], [grid_lat[0], grid_lat[-1]], [0, n-1])
        mast_carpan = _bilinear_matris_degeri(toplam_yerel_carpan, r, c)
        d["mast_arazi_carpani"] = float(np.clip(mast_carpan, 0.78, 1.22))
        d["normalize_hiz"] = float(d["hub_hizi"] / d["mast_arazi_carpani"])

    satirlar = []
    for i, lat in enumerate(grid_lat):
        for j, lon in enumerate(grid_lon):
            if not nokta_poligon_icinde(float(lon), float(lat), poligon):
                continue
            x, y = ileri(float(lon), float(lat))

            if len(direk_xy) == 1:
                bolgesel_hiz = float(direk_xy[0]["normalize_hiz"])
                temel_metod = "Tek direk topoğrafya-kalibrasyonu"
            else:
                mesafeler = np.array([max(np.hypot(x-d["x"], y-d["y"]), 100.0) for d in direk_xy], dtype=float)
                normalize_hizlar = np.array([d["normalize_hiz"] for d in direk_xy], dtype=float)
                # Uzak direğin etkisinin aşırı büyümemesi için yumuşatılmış mesafe ağırlığı.
                karakteristik = max(float(np.nanmedian(mesafeler)), 750.0)
                kalite_agirliklari = np.array([float(d.get("agirlik", 1.0)) for d in direk_xy], dtype=float)
                agirliklar = kalite_agirliklari / np.power(1.0 + mesafeler / karakteristik, float(idw_gucu))
                bolgesel_hiz = float(np.sum(agirliklar * normalize_hizlar) / np.sum(agirliklar))
                temel_metod = f"{len(direk_xy)} direk normalize bölgesel alan"

            carpan = float(toplam_yerel_carpan[i, j])
            hiz = float(bolgesel_hiz * carpan)
            en_yakin_direk_m = float(min(np.hypot(x-d["x"], y-d["y"]) for d in direk_xy))
            veri_guveni = float(np.clip(1.0 - en_yakin_direk_m / 15000.0, 0.25, 1.0))
            if not arazi_var:
                veri_guveni *= 0.75
            if "uygulanmadi" in puruzluluk_durumu.lower() or "erisilemedi" in puruzluluk_durumu.lower():
                veri_guveni *= 0.80
            satirlar.append({
                "lat": float(lat),
                "lon": float(lon),
                "Hub Rüzgar Hızı (m/s)": hiz,
                "Temel Hub Hızı (m/s)": float(bolgesel_hiz),
                "Kot (m)": float(z_mat[i, j]) if np.isfinite(z_mat[i, j]) else np.nan,
                "Arazi Çarpanı": float(arazi_carpani[i, j]),
                "Pürüzlülük Çarpanı": float(puruzluluk_carpani[i, j]),
                "Toplam Yerel Çarpan": carpan,
                "WorldCover Sınıfı": int(wc_sinif[i, j]) if np.isfinite(wc_sinif[i, j]) else np.nan,
                "Pürüzlülük z0 (m)": float(z0_mat[i, j]) if np.isfinite(z0_mat[i, j]) else np.nan,
                "Etkin Yönlü z0 (m)": float(etkin_z0[i, j]) if np.isfinite(etkin_z0[i, j]) else np.nan,
                "En Yakın Direk Mesafesi (m)": en_yakin_direk_m,
                "Model Güven Skoru": veri_guveni,
                "Yönlü Eğim": float(yonlu_egim[i, j]),
                "Upwind Engel Açısı (°)": float(engel_acisi[i, j]),
                "Sırtlık İndeksi": float(sirtlik[i, j]),
                "Harita Yöntemi": f"{temel_metod} + {arazi_durumu} + {puruzluluk_durumu}",
                "Arazi Veri Kaynağı": arazi_durumu,
                "Pürüzlülük Veri Kaynağı": puruzluluk_durumu,
                "Kullanılan Direk Sayısı": len(direk_xy),
            })

    sonuc = pd.DataFrame(satirlar)
    if not sonuc.empty:
        # Ölçüm direklerinden veri kalitesi ağırlıklı saha referansı oluştur.
        mast_hizlari = np.array([float(d["hub_hizi"]) for d in direk_xy], dtype=float)
        mast_agirliklari = np.array([float(d.get("agirlik", 1.0)) for d in direk_xy], dtype=float)
        mast_agirliklari = np.where(np.isfinite(mast_agirliklari) & (mast_agirliklari > 0), mast_agirliklari, 1.0)
        otomatik_referans = float(np.average(mast_hizlari, weights=mast_agirliklari))
        hedef_ortalama = float(referans_saha_hizi) if referans_saha_hizi is not None and np.isfinite(referans_saha_hizi) and referans_saha_hizi > 0 else otomatik_referans

        ham_ortalama = float(pd.to_numeric(sonuc["Hub Rüzgar Hızı (m/s)"], errors="coerce").mean())
        sonuc["Normalizasyon Öncesi Hız (m/s)"] = sonuc["Hub Rüzgar Hızı (m/s)"].astype(float)
        if ortalama_koru and np.isfinite(ham_ortalama) and ham_ortalama > 0:
            sonuc["Hub Rüzgar Hızı (m/s)"] *= hedef_ortalama / ham_ortalama

        # Sayısal artefaktları engelle; ölçümlere göre geniş fakat fiziksel bir bant kullan.
        olcum_min = float(np.nanmin(mast_hizlari))
        olcum_max = float(np.nanmax(mast_hizlari))
        alt = max(0.1, min(olcum_min * 0.72, hedef_ortalama * 0.75))
        ust = max(alt + 0.2, max(olcum_max * 1.28, hedef_ortalama * 1.25))
        sonuc["Hub Rüzgar Hızı (m/s)"] = sonuc["Hub Rüzgar Hızı (m/s)"].clip(alt, ust)

        # Kırpma ortalamayı az miktarda oynatırsa bir kez daha ortalamayı düzelt.
        son_ortalama = float(sonuc["Hub Rüzgar Hızı (m/s)"].mean())
        if ortalama_koru and np.isfinite(son_ortalama) and son_ortalama > 0:
            sonuc["Hub Rüzgar Hızı (m/s)"] *= hedef_ortalama / son_ortalama

        # Direkleri kesin kontrol noktası olarak koruyan yumuşak artık kalibrasyonu.
        # Her direğin model hatası Gaussian çekirdeklerle çevreye dağıtılır;
        # direk koordinatında nihai değer ölçülen hub hızına eşitlenir.
        if direk_xy:
            gx = np.array([ileri(float(lo), float(la))[0] for lo, la in zip(sonuc["lon"], sonuc["lat"])], dtype=float)
            gy = np.array([ileri(float(lo), float(la))[1] for lo, la in zip(sonuc["lon"], sonuc["lat"])], dtype=float)
            mevcut = sonuc["Hub Rüzgar Hızı (m/s)"].to_numpy(dtype=float)
            mast_spacing = []
            if len(direk_xy) > 1:
                for a in range(len(direk_xy)):
                    for b in range(a+1, len(direk_xy)):
                        mast_spacing.append(np.hypot(direk_xy[a]["x"]-direk_xy[b]["x"], direk_xy[a]["y"]-direk_xy[b]["y"]))
            etki_yaricapi = float(np.clip(np.nanmedian(mast_spacing) if mast_spacing else 1800.0, 900.0, 4500.0))
            pay = np.zeros_like(mevcut)
            payda = np.zeros_like(mevcut)
            for d in direk_xy:
                dist2 = (gx-d["x"])**2 + (gy-d["y"])**2
                model_mast = float(np.interp(d["lon"], [grid_lon[0], grid_lon[-1]], [0, n-1]))
                rr = float(np.interp(d["lat"], [grid_lat[0], grid_lat[-1]], [0, n-1]))
                # DataFrame yalnız poligon içini içerdiği için en yakın gerçek grid hücresini kullan.
                nearest = int(np.argmin(dist2))
                residual = float(d["hub_hizi"] - mevcut[nearest])
                w = np.exp(-0.5 * dist2 / max(etki_yaricapi**2, 1.0)) * float(d.get("agirlik", 1.0))
                pay += w * residual
                payda += w
            correction = np.divide(pay, payda, out=np.zeros_like(pay), where=payda > 1e-9)
            sonuc["Direk Kalibrasyon Düzeltmesi (m/s)"] = correction
            sonuc["Hub Rüzgar Hızı (m/s)"] = sonuc["Hub Rüzgar Hızı (m/s)"].to_numpy(dtype=float) + correction

            # Her direği sonuç tablosuna birebir kontrol kaydı olarak ekle.
            kontrol_satirlari = []
            for d in direk_xy:
                kontrol_satirlari.append({
                    "lat": float(d["lat"]), "lon": float(d["lon"]),
                    "Hub Rüzgar Hızı (m/s)": float(d["hub_hizi"]),
                    "Temel Hub Hızı (m/s)": float(d["hub_hizi"]),
                    "En Yakın Direk Mesafesi (m)": 0.0,
                    "Model Güven Skoru": 1.0,
                    "Harita Yöntemi": "Kesin direk kontrol noktası",
                    "Kullanılan Direk Sayısı": len(direk_xy),
                    "Nokta Türü": "Direk kontrol noktası",
                    "Model Hatası (m/s)": 0.0,
                })
            sonuc["Nokta Türü"] = sonuc.get("Nokta Türü", "Raster grid")
            sonuc["Model Hatası (m/s)"] = np.nan
            sonuc = pd.concat([sonuc, pd.DataFrame(kontrol_satirlari)], ignore_index=True, sort=False)

        final_ortalama = float(sonuc.loc[sonuc.get("Nokta Türü", "Raster grid") != "Direk kontrol noktası", "Hub Rüzgar Hızı (m/s)"].mean())
        sonuc["Referans Saha Ortalaması (m/s)"] = hedef_ortalama
        sonuc["Grid Ortalaması (m/s)"] = final_ortalama
        sonuc["Ortalama Farkı (m/s)"] = final_ortalama - hedef_ortalama
        sonuc["Ortalama Koruma"] = "Aktif" if ortalama_koru else "Pasif"
    return sonuc

def latlon_xy_donustur(poligon):
    """Küçük sahalar için lon/lat koordinatlarını yerel metre koordinatlarına çevirir."""
    lat0 = float(np.mean([p[1] for p in poligon]))
    lon0 = float(np.mean([p[0] for p in poligon]))
    r = 6371000.0
    cos_lat = np.cos(np.radians(lat0))

    def ileri(lon, lat):
        x = np.radians(lon - lon0) * r * cos_lat
        y = np.radians(lat - lat0) * r
        return float(x), float(y)

    def geri(x, y):
        lon = lon0 + np.degrees(x / (r * cos_lat))
        lat = lat0 + np.degrees(y / r)
        return float(lon), float(lat)

    return ileri, geri


def kare_calisma_alani_uret(merkez_poligon, alan_genisligi_km, merkez_konum=None):
    """Santral sınırının merkezinde, kullanıcı genişliğine göre kare çalışma alanı üretir."""
    if not merkez_poligon:
        return []
    genislik_m = max(float(alan_genisligi_km), 0.1) * 1000.0
    ileri, geri = latlon_xy_donustur(merkez_poligon)
    xy = np.array([ileri(lon, lat) for lon, lat in merkez_poligon], dtype=float)
    merkez_x = float(np.mean(xy[:, 0]))
    merkez_y = float(np.mean(xy[:, 1]))
    if merkez_konum is not None:
        merkez_x, merkez_y = ileri(float(merkez_konum[1]), float(merkez_konum[0]))
    yari = genislik_m / 2.0
    koseler_xy = [
        (merkez_x - yari, merkez_y - yari),
        (merkez_x + yari, merkez_y - yari),
        (merkez_x + yari, merkez_y + yari),
        (merkez_x - yari, merkez_y + yari),
        (merkez_x - yari, merkez_y - yari),
    ]
    return [geri(x, y) for x, y in koseler_xy]


def _kolon_adi_norm(ad):
    metin = str(ad or "").lower()
    metin = metin.replace("ı", "i").replace("ş", "s").replace("ğ", "g")
    metin = metin.replace("ü", "u").replace("ö", "o").replace("ç", "c")
    return re.sub(r"[^a-z0-9]+", "", metin)


def _kolon_sira_no(ad):
    n = _kolon_adi_norm(ad)
    # WS1, WD2, WindDir1, WindSpeed2 gibi isimlerde sensör sıra numarasını yakala.
    m = re.search(r"(?:ws|wd|windspeed|winddir|winddirection|direction|dir)([1-9])", n)
    if m:
        return int(m.group(1))
    return None


def _yon_hiz_kolon_ciftleri_bul(veri, sensor_yukseklikleri=None):
    """Gerçek ortalama yön kanallarını uygun rüzgâr hızı kanallarıyla eşler.

    WD *_Max / *_Std / *_Min kolonları yön frekansı değildir ve özellikle dışlanır.
    Kurulum raporunda sensör yükseklikleri varsa yön sensörü, yüksekliği en yakın
    WS sensörüyle eşleştirilir (örn. WD1=80 m -> WS2=80 m; WD2=40 m -> WS4=40 m).
    """
    kolonlar = list(veri.columns)
    yuk = sensor_yukseklikleri or {}

    def yon_mu(k):
        n = _kolon_adi_norm(k)
        if any(x in n for x in ('max', 'min', 'std', 'stdev', 'sd', 'gust')):
            return False
        temel = (
            n.startswith('wd') or n.startswith('winddir') or
            'winddirection' in n or n.startswith('direction') or n.startswith('dir')
        )
        # Avg/Mean açıkça varsa kabul et; yalnız tek yön kolonu varsa suffixsiz adı da destekle.
        return temel

    def hiz_mu(k):
        n = _kolon_adi_norm(k)
        if any(x in n for x in ('max', 'min', 'std', 'stdev', 'sd', 'gust')):
            return False
        if yon_mu(k):
            return False
        return n.startswith('ws') or n.startswith('windspeed') or ('wind' in n and 'speed' in n)

    yonlar = [k for k in kolonlar if yon_mu(k)]
    hizlar = [k for k in kolonlar if hiz_mu(k)]

    # Ortalama kolonları ilk sıraya al.
    yonlar.sort(key=lambda k: (0 if any(x in _kolon_adi_norm(k) for x in ('avg','mean')) else 1, str(k).lower()))
    hizlar.sort(key=lambda k: (0 if any(x in _kolon_adi_norm(k) for x in ('avg','mean')) else 1, str(k).lower()))

    # Aynı sensörün Avg/Mean'i varken suffixsiz/alternatif türevleri tekrarlama.
    sonuc_yon=[]
    gorulen_no=set()
    for k in yonlar:
        no=_kolon_sira_no(k)
        n=_kolon_adi_norm(k)
        if no is not None and no in gorulen_no and not ('avg' in n or 'mean' in n):
            continue
        sonuc_yon.append(k)
        if no is not None:
            gorulen_no.add(no)
    yonlar=sonuc_yon

    sonuc=[]
    kullanilan_hiz=set()
    for yon in yonlar:
        no=_kolon_sira_no(yon)
        yon_yuk=None
        if no is not None:
            for aday in (f'WD{no}_Avg', f'WD{no}', yon):
                try:
                    val=float(yuk.get(aday, 0.0) or 0.0)
                    if val > 0:
                        yon_yuk=val; break
                except Exception:
                    pass

        hiz=None
        # En doğru eşleştirme: kurulum raporundaki fiziksel yükseklik.
        if yon_yuk is not None:
            adaylar=[]
            for hkol in hizlar:
                hno=_kolon_sira_no(hkol)
                h_yuk=0.0
                if hno is not None:
                    for anahtar in (f'WS{hno}_Avg', f'WS{hno}', hkol):
                        try:
                            h_yuk=float(yuk.get(anahtar, 0.0) or 0.0)
                            if h_yuk > 0: break
                        except Exception:
                            h_yuk=0.0
                if h_yuk > 0:
                    adaylar.append((abs(h_yuk-yon_yuk), hkol))
            if adaylar:
                hiz=min(adaylar, key=lambda x:x[0])[1]

        # Yükseklik yoksa aynı sıra numarasını kullan.
        if hiz is None and no is not None:
            hiz=next((h for h in hizlar if _kolon_sira_no(h)==no), None)
        # Son fallback: henüz kullanılmamış ilk ortalama hız kolonu.
        if hiz is None:
            hiz=next((h for h in hizlar if h not in kullanilan_hiz), None)
        if hiz is not None:
            sonuc.append((str(yon), yon, hiz))
            kullanilan_hiz.add(hiz)
    return sonuc


def hakim_ruzgar_yonu_hesapla(veri):
    """Bulunabilen ilk geçerli yön kolonundan dairesel ortalama hakim yönü döndürür."""
    ciftler = _yon_hiz_kolon_ciftleri_bul(veri)
    if not ciftler:
        return 270.0
    yon_kolonu = ciftler[0][1]
    yon = pd.to_numeric(veri[yon_kolonu], errors="coerce")
    yon = yon[(yon >= 0) & (yon < 360)].dropna()
    if yon.empty:
        return 270.0
    radyan = np.radians(yon.to_numpy(dtype=float))
    sin_ort = np.mean(np.sin(radyan))
    cos_ort = np.mean(np.cos(radyan))
    return float((np.degrees(np.arctan2(sin_ort, cos_ort)) + 360.0) % 360.0)


def turbin_yerlesimi_uret(poligon, turbin_sayisi, rotor_capi_m, ruzgar_yonu_deg,
                           capraz_d=2.5, ruzgar_alti_d=6.0):
    """
    Santral poligonu içinde gerçek yönlü elips metoduyla otomatik ön yerleşim üretir.

    Her seçilmiş türbinin çevresinde, hakim rüzgara dik yarı ekseni
    capraz_d * D ve hakim rüzgar doğrultusundaki yarı ekseni
    ruzgar_alti_d * D olan bir yasak elips tanımlanır. Yeni aday yalnızca
    bütün mevcut elipslerin dışında kalıyorsa kabul edilir.
    """
    ileri, geri = latlon_xy_donustur(poligon)
    xy_poligon = np.array([ileri(lon, lat) for lon, lat in poligon], dtype=float)

    # Rüzgarın geldiği yönü yerel koordinat sisteminin y eksenine çevir.
    aci = np.radians(270.0 - float(ruzgar_yonu_deg))
    c, s = np.cos(aci), np.sin(aci)

    def dondur(x, y):
        return c * x - s * y, s * x + c * y

    def ters_dondur(xr, yr):
        return c * xr + s * yr, -s * xr + c * yr

    rot = np.array([dondur(x, y) for x, y in xy_poligon], dtype=float)
    x_min, y_min = rot.min(axis=0)
    x_max, y_max = rot.max(axis=0)

    yaricap_x = float(capraz_d) * float(rotor_capi_m)
    yaricap_y = float(ruzgar_alti_d) * float(rotor_capi_m)
    if yaricap_x <= 0 or yaricap_y <= 0:
        return []

    # Elips yöntemi diyagonal yerleşimlere izin verdiği için aday ağı,
    # eksen mesafelerinden daha sık üretilir. Nihai uygunluk elips denklemiyle kontrol edilir.
    aday_adimi = max(min(yaricap_x, yaricap_y) / 2.0, float(rotor_capi_m) * 0.5)
    adaylar = []
    for yr in np.arange(y_min, y_max + aday_adimi, aday_adimi):
        for xr in np.arange(x_min, x_max + aday_adimi, aday_adimi):
            x, y = ters_dondur(xr, yr)
            lon, lat = geri(x, y)
            if nokta_poligon_icinde(lon, lat, poligon):
                adaylar.append({
                    "lon": lon, "lat": lat, "x": x, "y": y,
                    "xr": float(xr), "yr": float(yr)
                })

    if not adaylar:
        return []

    # Kompakt yerleşim için merkezden dışarı doğru ilerle.
    merkez_x = float(np.mean(xy_poligon[:, 0]))
    merkez_y = float(np.mean(xy_poligon[:, 1]))
    adaylar.sort(key=lambda p: (p["x"] - merkez_x) ** 2 + (p["y"] - merkez_y) ** 2)

    secilen = []
    for aday in adaylar:
        uygun = True
        for mevcut in secilen:
            dx = aday["xr"] - mevcut["xr"]
            dy = aday["yr"] - mevcut["yr"]
            elips_degeri = (dx / yaricap_x) ** 2 + (dy / yaricap_y) ** 2
            if elips_degeri < 1.0 - 1e-9:
                uygun = False
                break
        if uygun:
            secilen.append(aday)
            if len(secilen) >= int(turbin_sayisi):
                break

    for i, nokta in enumerate(secilen, start=1):
        nokta["ad"] = f"T{i}"
    return secilen


def yerlesim_mesafe_kontrolu(turbinler, rotor_capi_m, capraz_d=2.5, ruzgar_alti_d=6.0):
    """Gerçek 2,5D x 6D yönlü elips metoduyla türbin çiftlerini denetler."""
    ihlaller = []
    yaricap_x = float(capraz_d) * float(rotor_capi_m)
    yaricap_y = float(ruzgar_alti_d) * float(rotor_capi_m)
    if yaricap_x <= 0 or yaricap_y <= 0:
        return ihlaller

    for i in range(len(turbinler)):
        for j in range(i + 1, len(turbinler)):
            dx = abs(turbinler[i]["xr"] - turbinler[j]["xr"])
            dy = abs(turbinler[i]["yr"] - turbinler[j]["yr"])
            elips_degeri = (dx / yaricap_x) ** 2 + (dy / yaricap_y) ** 2
            if elips_degeri < 1.0 - 1e-9:
                ihlaller.append({
                    "Türbin 1": turbinler[i]["ad"],
                    "Türbin 2": turbinler[j]["ad"],
                    "Çapraz mesafe (D)": dx / float(rotor_capi_m),
                    "Rüzgar-altı mesafe (D)": dy / float(rotor_capi_m),
                    "Elips değeri": elips_degeri
                })
    return ihlaller


def jensen_wake_kaybi_hesapla(turbinler, rotor_capi_m, ct=0.80, wake_k=0.075):
    """Basitleştirilmiş Jensen/Park yaklaşımıyla türbin bazlı ön wake kaybı tahmini."""
    if not turbinler:
        return [], 0.0
    sonuc = []
    d = float(rotor_capi_m)
    for hedef in turbinler:
        kare_toplam = 0.0
        for kaynak in turbinler:
            if kaynak["ad"] == hedef["ad"]:
                continue
            x = hedef["yr"] - kaynak["yr"]
            if x <= 0:
                continue
            y = abs(hedef["xr"] - kaynak["xr"])
            wake_yaricap = d / 2.0 + float(wake_k) * x
            if y <= wake_yaricap:
                deficit = (1.0 - np.sqrt(1.0 - float(ct))) / (1.0 + 2.0 * float(wake_k) * x / d) ** 2
                kare_toplam += deficit ** 2
        toplam_deficit = min(float(np.sqrt(kare_toplam)), 0.45)
        guc_kaybi = 1.0 - (1.0 - toplam_deficit) ** 3
        sonuc.append({
            "Türbin": hedef["ad"],
            "Rüzgar hızı kaybı (%)": toplam_deficit * 100.0,
            "Yaklaşık güç kaybı (%)": guc_kaybi * 100.0
        })
    ortalama = float(np.mean([r["Yaklaşık güç kaybı (%)"] for r in sonuc])) if sonuc else 0.0
    return sonuc, ortalama



# ============================================================
# RÜZGAR GRIDİ VE MİKROSITING
# ============================================================

def kml_kmz_tum_poligonlari_oku(yuklenen_dosya):
    """
    KML/KMZ içindeki bütün KML dosyalarını tarar ve bütün Polygon halkalarını döndürür.
    Yasak alan kullanımında hem dış halkalar hem de iç halkalar ayrı poligonlar olarak alınır.
    """
    if yuklenen_dosya is None:
        return []

    tum_poligonlar = []
    hatalar = []
    for kaynak_adi, kml_bytes in _kml_kmz_kaynaklarini_oku(yuklenen_dosya):
        try:
            dis_poligonlar, ic_poligonlar = _kml_bytes_poligonlarini_oku(kml_bytes)
            tum_poligonlar.extend(dis_poligonlar)
            tum_poligonlar.extend(ic_poligonlar)
        except ValueError as hata:
            hatalar.append(f"{kaynak_adi}: {hata}")

    if not tum_poligonlar:
        ayrinti = " | ".join(hatalar[:3])
        mesaj = "KMZ/KML içinde geçerli Polygon koordinatı bulunamadı."
        if ayrinti:
            mesaj += f" Ayrıntı: {ayrinti}"
        raise ValueError(mesaj)

    return tum_poligonlar


def nokta_segment_mesafesi(px, py, ax, ay, bx, by):
    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay
    payda = abx * abx + aby * aby
    if payda <= 1e-12:
        return float(np.hypot(px - ax, py - ay))
    t = max(0.0, min(1.0, (apx * abx + apy * aby) / payda))
    qx, qy = ax + t * abx, ay + t * aby
    return float(np.hypot(px - qx, py - qy))


def sinira_mesafe_m(lon, lat, poligon, ileri=None):
    if ileri is None:
        ileri, _ = latlon_xy_donustur(poligon)
    px, py = ileri(lon, lat)
    xy = [ileri(p_lon, p_lat) for p_lon, p_lat in poligon]
    return min(
        nokta_segment_mesafesi(px, py, xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1])
        for i in range(len(xy) - 1)
    )


def grid_saha_filtrele(grid, ana_poligon, yasak_poligonlar=None, setback_m=0.0, max_egim_deg=None):
    """Gridi sınır, setback, yasak alan ve varsa eğim kriterleriyle filtreler."""
    yasak_poligonlar = yasak_poligonlar or []
    ileri, _ = latlon_xy_donustur(ana_poligon)
    satirlar = []
    for _, satir in grid.iterrows():
        lon, lat = float(satir['lon']), float(satir['lat'])
        if not nokta_poligon_icinde(lon, lat, ana_poligon):
            continue
        if setback_m > 0 and sinira_mesafe_m(lon, lat, ana_poligon, ileri) < float(setback_m):
            continue
        if any(nokta_poligon_icinde(lon, lat, p) for p in yasak_poligonlar):
            continue
        if max_egim_deg is not None and 'Eğim (°)' in grid.columns:
            egim = satir.get('Eğim (°)')
            if pd.notna(egim) and float(egim) > float(max_egim_deg):
                continue
        satirlar.append(satir.to_dict())
    return pd.DataFrame(satirlar)


def ruzgar_eksenleri(ruzgar_yonu_deg):
    """Meteorolojik geliş yönünü rüzgar-altı ve çapraz birim vektörlerine çevirir."""
    akis_deg = (float(ruzgar_yonu_deg) + 180.0) % 360.0
    theta = np.radians(90.0 - akis_deg)
    along = np.array([np.cos(theta), np.sin(theta)], dtype=float)
    cross = np.array([-along[1], along[0]], dtype=float)
    return along, cross


def micrositing_yerlesimi_uret(grid, poligon, turbin_sayisi, rotor_capi_m, ruzgar_yonu_deg,
                                capraz_d=2.5, ruzgar_alti_d=6.0):
    """En yüksek rüzgar hücrelerinden başlayarak gerçek yönlü elips kontrollü yerleşim."""
    if grid is None or grid.empty:
        return []

    ileri, _ = latlon_xy_donustur(poligon)
    along_vec, cross_vec = ruzgar_eksenleri(ruzgar_yonu_deg)
    adaylar = grid.sort_values('Hub Rüzgar Hızı (m/s)', ascending=False).copy()
    secilen = []
    yari_eksen_cross = float(capraz_d) * float(rotor_capi_m)
    yari_eksen_along = float(ruzgar_alti_d) * float(rotor_capi_m)

    if yari_eksen_cross <= 0 or yari_eksen_along <= 0:
        return []

    for _, satir in adaylar.iterrows():
        x, y = ileri(float(satir['lon']), float(satir['lat']))
        uygun = True
        for mevcut in secilen:
            delta = np.array([x - mevcut['x'], y - mevcut['y']], dtype=float)
            along = float(np.dot(delta, along_vec))
            cross = float(np.dot(delta, cross_vec))
            elips_degeri = (
                (cross / yari_eksen_cross) ** 2
                + (along / yari_eksen_along) ** 2
            )
            if elips_degeri < 1.0 - 1e-9:
                uygun = False
                break
        if not uygun:
            continue

        kayit = {
            'ad': f'T{len(secilen) + 1}',
            'lon': float(satir['lon']),
            'lat': float(satir['lat']),
            'x': float(x),
            'y': float(y),
            'xr': float(np.dot(np.array([x, y]), cross_vec)),
            'yr': float(np.dot(np.array([x, y]), along_vec)),
            'hub_hizi': float(satir['Hub Rüzgar Hızı (m/s)'])
        }
        if 'Eğim (°)' in satir and pd.notna(satir.get('Eğim (°)')):
            kayit['egim'] = float(satir['Eğim (°)'])
        if 'TI' in satir and pd.notna(satir.get('TI')):
            kayit['ti'] = float(satir['TI'])
        secilen.append(kayit)
        if len(secilen) >= int(turbin_sayisi):
            break
    return secilen





def _kolon_norm_turbin_excel(ad):
    metin = str(ad or "").strip().lower()
    metin = (
        metin.replace("ı", "i").replace("ş", "s").replace("ğ", "g")
        .replace("ü", "u").replace("ö", "o").replace("ç", "c")
    )
    return re.sub(r"[^a-z0-9]+", "", metin)




TURKIYE_IL_BOYLAMLARI = {
    "Adana": 35.33, "Adıyaman": 38.28, "Afyonkarahisar": 30.54, "Ağrı": 43.05,
    "Aksaray": 34.03, "Amasya": 35.83, "Ankara": 32.86, "Antalya": 30.70,
    "Ardahan": 42.70, "Artvin": 41.82, "Aydın": 27.84, "Balıkesir": 27.89,
    "Bartın": 32.34, "Batman": 41.13, "Bayburt": 40.23, "Bilecik": 29.98,
    "Bingöl": 40.50, "Bitlis": 42.11, "Bolu": 31.61, "Burdur": 30.29,
    "Bursa": 29.06, "Çanakkale": 26.41, "Çankırı": 33.62, "Çorum": 34.95,
    "Denizli": 29.09, "Diyarbakır": 40.23, "Düzce": 31.16, "Edirne": 26.56,
    "Elazığ": 39.22, "Erzincan": 39.49, "Erzurum": 41.27, "Eskişehir": 30.52,
    "Gaziantep": 37.38, "Giresun": 38.39, "Gümüşhane": 39.48, "Hakkari": 43.74,
    "Hatay": 36.16, "Iğdır": 44.04, "Isparta": 30.55, "İstanbul": 28.98,
    "İzmir": 27.14, "Kahramanmaraş": 36.93, "Karabük": 32.63, "Karaman": 33.22,
    "Kars": 43.10, "Kastamonu": 33.78, "Kayseri": 35.49, "Kırıkkale": 33.52,
    "Kırklareli": 27.22, "Kırşehir": 34.16, "Kilis": 37.12, "Kocaeli": 29.93,
    "Konya": 32.49, "Kütahya": 29.98, "Malatya": 38.31, "Manisa": 27.43,
    "Mardin": 40.74, "Mersin": 34.63, "Muğla": 28.36, "Muş": 41.49,
    "Nevşehir": 34.72, "Niğde": 34.68, "Ordu": 37.88, "Osmaniye": 36.25,
    "Rize": 40.52, "Sakarya": 30.40, "Samsun": 36.33, "Şanlıurfa": 38.80,
    "Siirt": 41.94, "Sinop": 35.15, "Sivas": 37.02, "Şırnak": 42.46,
    "Tekirdağ": 27.51, "Tokat": 36.55, "Trabzon": 39.72, "Tunceli": 39.55,
    "Uşak": 29.41, "Van": 43.38, "Yalova": 29.27, "Yozgat": 34.81,
    "Zonguldak": 31.79,
}


def _ilden_utm_zonu_ve_tm3_meridyeni(il_adi):
    lon = float(TURKIYE_IL_BOYLAMLARI.get(str(il_adi), 32.86))
    # UTM 6° zonu
    zone = int(math.floor((lon + 180.0) / 6.0) + 1)
    zone = max(35, min(38, zone))
    # Türkiye TM3 merkezi meridyenleri: 27,30,33,36,39,42,45
    cm = int(round(lon / 3.0) * 3)
    cm = max(27, min(45, cm))
    return zone, cm

def _inverse_transverse_mercator(x, y, a, inv_f, lon0_deg, k0=1.0, false_easting=500000.0, false_northing=0.0):
    """Inverse Transverse Mercator. Returns geodetic lat/lon in degrees."""
    f = 1.0 / float(inv_f)
    e2 = f * (2.0 - f)
    ep2 = e2 / (1.0 - e2)

    M = (float(y) - false_northing) / k0
    mu = M / (a * (1.0 - e2/4.0 - 3.0*e2**2/64.0 - 5.0*e2**3/256.0))

    e1 = (1.0 - math.sqrt(1.0 - e2)) / (1.0 + math.sqrt(1.0 - e2))
    j1 = 3.0*e1/2.0 - 27.0*e1**3/32.0
    j2 = 21.0*e1**2/16.0 - 55.0*e1**4/32.0
    j3 = 151.0*e1**3/96.0
    j4 = 1097.0*e1**4/512.0

    phi1 = (
        mu
        + j1 * math.sin(2.0*mu)
        + j2 * math.sin(4.0*mu)
        + j3 * math.sin(6.0*mu)
        + j4 * math.sin(8.0*mu)
    )

    sin1 = math.sin(phi1)
    cos1 = math.cos(phi1)
    tan1 = math.tan(phi1)

    N1 = a / math.sqrt(1.0 - e2*sin1*sin1)
    R1 = a * (1.0 - e2) / ((1.0 - e2*sin1*sin1) ** 1.5)
    T1 = tan1*tan1
    C1 = ep2*cos1*cos1
    D = (float(x) - false_easting) / (N1 * k0)

    lat = phi1 - (N1*tan1/R1) * (
        D**2/2.0
        - (5.0 + 3.0*T1 + 10.0*C1 - 4.0*C1**2 - 9.0*ep2) * D**4 / 24.0
        + (61.0 + 90.0*T1 + 298.0*C1 + 45.0*T1**2 - 252.0*ep2 - 3.0*C1**2) * D**6 / 720.0
    )

    lon0 = math.radians(float(lon0_deg))
    lon = lon0 + (
        D
        - (1.0 + 2.0*T1 + C1) * D**3 / 6.0
        + (5.0 - 2.0*C1 + 28.0*T1 - 3.0*C1**2 + 8.0*ep2 + 24.0*T1**2) * D**5 / 120.0
    ) / cos1

    return math.degrees(lat), math.degrees(lon)


def _geodetic_to_ecef(lat_deg, lon_deg, h, a, inv_f):
    f = 1.0 / float(inv_f)
    e2 = f * (2.0 - f)
    lat = math.radians(float(lat_deg))
    lon = math.radians(float(lon_deg))
    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    N = a / math.sqrt(1.0 - e2*sin_lat*sin_lat)
    X = (N + h) * cos_lat * math.cos(lon)
    Y = (N + h) * cos_lat * math.sin(lon)
    Z = (N*(1.0 - e2) + h) * sin_lat
    return X, Y, Z


def _ecef_to_geodetic(X, Y, Z, a, inv_f):
    f = 1.0 / float(inv_f)
    e2 = f * (2.0 - f)
    lon = math.atan2(Y, X)
    p = math.hypot(X, Y)

    lat = math.atan2(Z, p*(1.0 - e2))
    for _ in range(12):
        sin_lat = math.sin(lat)
        N = a / math.sqrt(1.0 - e2*sin_lat*sin_lat)
        h = p / max(math.cos(lat), 1e-15) - N
        yeni = math.atan2(Z, p*(1.0 - e2*N/(N + h)))
        if abs(yeni - lat) < 1e-13:
            lat = yeni
            break
        lat = yeni

    return math.degrees(lat), math.degrees(lon)


def _ed50_geodetic_to_wgs84(lat_deg, lon_deg):
    """Turkey-specific ED50 -> WGS84 approximation using EPSG transformation 1784."""
    # ED50 / International 1924
    X, Y, Z = _geodetic_to_ecef(lat_deg, lon_deg, 0.0, 6378388.0, 297.0)

    # EPSG:1784 position-vector parameters for Türkiye:
    # dx=-84.1 m, dy=-101.8 m, dz=-129.7 m, rx=0, ry=0,
    # rz=+0.468 arcsec, scale=+1.05 ppm.
    dx, dy, dz = -84.1, -101.8, -129.7
    rx_sec, ry_sec, rz_sec = 0.0, 0.0, 0.468
    ds_ppm = 1.05
    sec_to_rad = math.pi / (180.0 * 3600.0)
    rx = rx_sec * sec_to_rad
    ry = ry_sec * sec_to_rad
    rz = rz_sec * sec_to_rad
    m = 1.0 + ds_ppm * 1e-6

    X2 = dx + m*X - rz*Y + ry*Z
    Y2 = dy + rz*X + m*Y - rx*Z
    Z2 = dz - ry*X + rx*Y + m*Z

    # WGS84
    return _ecef_to_geodetic(X2, Y2, Z2, 6378137.0, 298.257223563)


def _turbin_xy_to_wgs84(x, y, koordinat_sistemi, ed50_zone=36, itrf_cm=36, custom_epsg=4326):
    secim = str(koordinat_sistemi or "").strip()

    if secim == "ED50 / UTM 6°":
        zone = int(ed50_zone)
        if zone not in {35, 36, 37, 38}:
            raise ValueError("ED50 için UTM zonu 35, 36, 37 veya 38 olmalıdır.")
        lon0 = zone * 6 - 183
        lat_ed50, lon_ed50 = _inverse_transverse_mercator(
            x, y,
            a=6378388.0,
            inv_f=297.0,
            lon0_deg=lon0,
            k0=0.9996,
            false_easting=500000.0,
            false_northing=0.0,
        )
        lat_wgs, lon_wgs = _ed50_geodetic_to_wgs84(lat_ed50, lon_ed50)
        return lon_wgs, lat_wgs

    if secim == "ITRF96 / TM3":
        cm = int(itrf_cm)
        if cm not in {27, 30, 33, 36, 39, 42, 45}:
            raise ValueError("ITRF96/TM3 merkezi meridyeni 27, 30, 33, 36, 39, 42 veya 45 olmalıdır.")
        lat, lon = _inverse_transverse_mercator(
            x, y,
            a=6378137.0,
            inv_f=298.257222101,  # GRS80
            lon0_deg=cm,
            k0=1.0,
            false_easting=500000.0,
            false_northing=0.0,
        )
        # ITRF96/GRS80 ile WGS84 farkı bu uygulama seviyesinde ihmal edilebilir.
        return lon, lat

    if secim == "Özel EPSG":
        # Kurumsal Windows'ta pyproj DLL'i engellenebildiği için özel EPSG'yi
        # yalnız pyproj gerçekten çalışıyorsa destekle.
        try:
            from pyproj import Transformer
            transformer = Transformer.from_crs(f"EPSG:{int(custom_epsg)}", "EPSG:4326", always_xy=True)
            return transformer.transform(float(x), float(y))
        except Exception as hata:
            raise ValueError(
                "Özel EPSG dönüşümü için pyproj gerekir; bu bilgisayarda Windows ilkesi pyproj DLL'ini engelliyor. "
                "ED50/UTM 6° veya ITRF96/TM3 seçerseniz pyproj gerekmez."
            ) from hata

    raise ValueError(f"Desteklenmeyen koordinat sistemi: {secim}")


def _turbin_kaynak_crs_olustur(koordinat_sistemi, ed50_zone=36, itrf_cm=36, custom_epsg=4326):
    """Returns a lightweight CRS descriptor; ED50/ITRF conversions are pure Python."""
    secim = str(koordinat_sistemi or "").strip()

    if secim == "WGS84 / Enlem-Boylam":
        return {"type": "wgs84"}, "WGS84 · EPSG:4326"

    if secim == "ED50 / UTM 6°":
        zone = int(ed50_zone)
        if zone not in {35, 36, 37, 38}:
            raise ValueError("ED50 için UTM zonu 35, 36, 37 veya 38 olmalıdır.")
        epsg = 23000 + zone
        return {"type": "ed50_utm", "zone": zone}, f"ED50 / UTM zone {zone}N · EPSG:{epsg}"

    if secim == "ITRF96 / TM3":
        cm = int(itrf_cm)
        if cm not in {27, 30, 33, 36, 39, 42, 45}:
            raise ValueError("ITRF96/TM3 merkezi meridyeni 27, 30, 33, 36, 39, 42 veya 45 olmalıdır.")
        return {"type": "itrf96_tm3", "cm": cm}, f"ITRF96 / TM3 · merkezi meridyen {cm}°"

    if secim == "Özel EPSG":
        epsg = int(custom_epsg)
        if epsg <= 0:
            raise ValueError("EPSG kodu pozitif bir sayı olmalıdır.")
        return {"type": "epsg", "epsg": epsg}, f"EPSG:{epsg}"

    raise ValueError(f"Desteklenmeyen koordinat sistemi: {secim}")

def turbin_excel_noktalarini_oku(
    uploaded_file,
    koordinat_sistemi="WGS84 / Enlem-Boylam",
    ed50_zone=36,
    itrf_cm=36,
    custom_epsg=4326,
):
    """Excel/CSV'den türbin noktalarını okur ve WGS84 enlem-boylama dönüştürür.

    WGS84 modunda: Enlem/Boylam (Latitude/Longitude, Lat/Lon) sütunları beklenir.
    Projeksiyonlu modlarda: X/Y veya Easting/Northing sütunları beklenir.
    """
    if uploaded_file is None:
        return [], [], None

    ad = str(uploaded_file.name or "")
    uzanti = Path(ad).suffix.lower()
    ham = uploaded_file.getvalue()

    try:
        if uzanti == ".xlsx":
            # pandas.read_excel openpyxl'e bağımlıdır. Uygulamanın çalıştığı
            # ortamda openpyxl ayrıca kurulu olmak zorunda kalmasın diye
            # XLSX'i Python stdlib (zipfile+xml) ile doğrudan okuyoruz.
            import zipfile
            import xml.etree.ElementTree as ET

            def _xlsx_hucre_degeri(cell, shared_strings, ns):
                cell_type = cell.attrib.get("t")
                v = cell.find("m:v", ns)
                if cell_type == "inlineStr":
                    t = cell.find(".//m:t", ns)
                    return t.text if t is not None else ""
                if v is None:
                    return None
                raw = v.text
                if cell_type == "s":
                    try:
                        return shared_strings[int(raw)]
                    except Exception:
                        return raw
                if cell_type in {"str", "b"}:
                    return raw
                try:
                    num = float(raw)
                    return int(num) if num.is_integer() else num
                except Exception:
                    return raw

            with zipfile.ZipFile(io.BytesIO(ham)) as zf:
                ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
                shared_strings = []
                if "xl/sharedStrings.xml" in zf.namelist():
                    root_ss = ET.fromstring(zf.read("xl/sharedStrings.xml"))
                    for si in root_ss.findall("m:si", ns):
                        shared_strings.append("".join(t.text or "" for t in si.findall(".//m:t", ns)))

                sheet_name = next(
                    (n for n in zf.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")),
                    None,
                )
                if sheet_name is None:
                    raise ValueError("XLSX içinde çalışma sayfası bulunamadı.")

                root = ET.fromstring(zf.read(sheet_name))
                rows = []
                for row in root.findall(".//m:sheetData/m:row", ns):
                    vals = []
                    for cell in row.findall("m:c", ns):
                        ref = cell.attrib.get("r", "A1")
                        letters = re.match(r"[A-Z]+", ref)
                        if not letters:
                            continue
                        col_letters = letters.group(0)
                        col_idx = 0
                        for ch in col_letters:
                            col_idx = col_idx * 26 + (ord(ch) - 64)
                        while len(vals) < col_idx:
                            vals.append(None)
                        vals[col_idx - 1] = _xlsx_hucre_degeri(cell, shared_strings, ns)
                    rows.append(vals)

            max_cols = max((len(r) for r in rows), default=0)
            rows = [r + [None] * (max_cols - len(r)) for r in rows]
            if not rows:
                raise ValueError("XLSX içinde veri bulunamadı.")

            # İlk satır başlık mı veri mi? T1 / 553137 / 4554050 gibi bir
            # satırsa başlıksız Excel kabul edilir.
            ilk = rows[0]
            norm_ilk = [_kolon_norm_turbin_excel(v) for v in ilk if v is not None]
            baslik_ipucu = any(
                n in {"enlem", "boylam", "latitude", "longitude", "lat", "lon",
                      "lng", "x", "y", "easting", "northing", "turbin", "turbine",
                      "name", "id", "wtg"}
                for n in norm_ilk
            )
            if baslik_ipucu:
                headers = [str(v).strip() if v is not None else f"Kolon{i+1}" for i, v in enumerate(ilk)]
                df = pd.DataFrame(rows[1:], columns=headers)
            else:
                # Yaygın saha teslim formatı: Türbin adı | X | Y
                headers = ["Türbin", "X", "Y"] + [f"Kolon{i}" for i in range(4, max_cols + 1)]
                df = pd.DataFrame(rows, columns=headers[:max_cols])

        elif uzanti == ".xls":
            # Eski binary XLS için pandas/xlrd gerekir; kullanıcıya net mesaj ver.
            try:
                df = pd.read_excel(io.BytesIO(ham))
            except ImportError as hata:
                raise ValueError(
                    "Eski .xls biçimi için ek Excel motoru gerekiyor. Dosyayı .xlsx olarak kaydedip tekrar yükleyin."
                ) from hata
        elif uzanti == ".csv":
            try:
                df = pd.read_csv(io.BytesIO(ham), sep=None, engine="python")
            except Exception:
                df = pd.read_csv(io.BytesIO(ham))
        else:
            raise ValueError("Yalnızca XLSX, XLS veya CSV yükleyin.")
    except Exception as hata:
        raise ValueError(f"Türbin koordinat dosyası okunamadı: {hata}") from hata

    if df is None or df.empty:
        raise ValueError("Yüklenen dosyada satır bulunamadı.")

    kolon_haritasi = {_kolon_norm_turbin_excel(k): k for k in df.columns}

    def ilk_eslesen(adaylar):
        for aday in adaylar:
            if aday in kolon_haritasi:
                return kolon_haritasi[aday]
        for norm, asil in kolon_haritasi.items():
            if any(a == norm or (len(a) >= 4 and a in norm) for a in adaylar):
                return asil
        return None

    projected = str(koordinat_sistemi) != "WGS84 / Enlem-Boylam"

    if not projected:
        y_col = ilk_eslesen(["enlem", "latitude", "lat"])
        x_col = ilk_eslesen(["boylam", "longitude", "lon", "lng"])
        if y_col is None or x_col is None:
            raise ValueError(
                "WGS84 için Enlem ve Boylam sütunları bulunamadı. "
                "Sütun adlarını 'Enlem' ve 'Boylam' (veya Latitude/Longitude) yapın."
            )
    else:
        x_col = ilk_eslesen([
            "x", "easting", "east", "dogu", "dogukoordinati",
            "xkoordinati", "xcoord", "xcoordinate"
        ])
        y_col = ilk_eslesen([
            "y", "northing", "north", "kuzey", "kuzeykoordinati",
            "ykoordinati", "ycoord", "ycoordinate"
        ])
        if x_col is None or y_col is None:
            raise ValueError(
                "Projeksiyonlu koordinat sistemi için X/Y (veya Easting/Northing) "
                "sütunları bulunamadı."
            )

    ad_col = ilk_eslesen([
        "turbin", "turbine", "turbinadi", "turbinno", "name", "id", "wtg", "wtgid"
    ])

    kaynak_crs, crs_etiket = _turbin_kaynak_crs_olustur(
        koordinat_sistemi,
        ed50_zone=ed50_zone,
        itrf_cm=itrf_cm,
        custom_epsg=custom_epsg,
    )

    noktalar = []
    uyarilar = []

    for idx, satir in df.iterrows():
        xv = pd.to_numeric(pd.Series([satir.get(x_col)]), errors="coerce").iloc[0]
        yv = pd.to_numeric(pd.Series([satir.get(y_col)]), errors="coerce").iloc[0]

        if pd.isna(xv) or pd.isna(yv):
            uyarilar.append(f"{idx + 2}. satır: koordinat okunamadı.")
            continue

        try:
            x = float(xv)
            y = float(yv)
            if projected:
                lon, lat = _turbin_xy_to_wgs84(
                    x, y,
                    koordinat_sistemi=koordinat_sistemi,
                    ed50_zone=ed50_zone,
                    itrf_cm=itrf_cm,
                    custom_epsg=custom_epsg,
                )
            else:
                lat, lon = y, x
        except Exception:
            uyarilar.append(f"{idx + 2}. satır: koordinat dönüştürülemedi.")
            continue

        if not (np.isfinite(lat) and np.isfinite(lon)):
            uyarilar.append(f"{idx + 2}. satır: dönüşüm geçersiz sonuç verdi.")
            continue
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            uyarilar.append(f"{idx + 2}. satır: dönüştürülen koordinat aralık dışında.")
            continue

        turbin_adi = None
        if ad_col is not None:
            deger = satir.get(ad_col)
            if pd.notna(deger) and str(deger).strip():
                turbin_adi = str(deger).strip()

        noktalar.append({
            "lat": float(lat),
            "lon": float(lon),
            "ad": turbin_adi or f"T{len(noktalar) + 1}",
        })

    temiz = []
    gorulen = set()
    for nokta in noktalar:
        anahtar = (round(float(nokta["lat"]), 8), round(float(nokta["lon"]), 8))
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        temiz.append(nokta)

    return temiz, uyarilar, {
        "x_col": str(x_col),
        "y_col": str(y_col),
        "name_col": str(ad_col) if ad_col is not None else None,
        "row_count": int(len(df)),
        "valid_count": int(len(temiz)),
        "source_crs": crs_etiket,
        "target_crs": "WGS84 · EPSG:4326",
    }




def eksik_turbinleri_sahaya_ekle(mevcut_noktalar, hedef_sayi, santral_poligonu):
    """Hedef türbin sayısı mevcut noktadan büyükse saha içine başlangıç noktaları ekler."""
    noktalar = [dict(p) for p in (mevcut_noktalar or [])]
    hedef_sayi = int(max(0, hedef_sayi))
    if len(noktalar) >= hedef_sayi or not santral_poligonu:
        return noktalar

    try:
        lons = [float(p[0]) for p in santral_poligonu]
        lats = [float(p[1]) for p in santral_poligonu]
        lon_min, lon_max = min(lons), max(lons)
        lat_min, lat_max = min(lats), max(lats)

        # Düzenli aday grid üret; mevcut noktalardan mümkün olduğunca uzak olanları sırayla seç.
        adaylar = []
        ngrid = 24
        for iy in range(ngrid):
            lat = lat_min + (iy + 0.5) * (lat_max - lat_min) / ngrid
            for ix in range(ngrid):
                lon = lon_min + (ix + 0.5) * (lon_max - lon_min) / ngrid
                if nokta_poligon_icinde(lon, lat, santral_poligonu):
                    adaylar.append((lat, lon))

        def _uzaklik_skoru(lat, lon):
            if not noktalar:
                return 1e9
            cos_lat = max(abs(math.cos(math.radians(lat))), 1e-6)
            en_yakin = 1e18
            for p in noktalar:
                dy = (lat - float(p["lat"])) * 111320.0
                dx = (lon - float(p["lon"])) * 111320.0 * cos_lat
                en_yakin = min(en_yakin, dx*dx + dy*dy)
            return en_yakin

        while len(noktalar) < hedef_sayi and adaylar:
            lat, lon = max(adaylar, key=lambda q: _uzaklik_skoru(q[0], q[1]))
            noktalar.append({
                "lat": float(lat),
                "lon": float(lon),
                "ad": f"T{len(noktalar)+1}",
                "excel_lat": None,
                "excel_lon": None,
            })
            adaylar.remove((lat, lon))
    except Exception:
        pass
    return noktalar


def turbin_noktasini_metre_kaydir(nokta, dogu_m=0.0, kuzey_m=0.0):
    """WGS84 türbin noktasını küçük saha mesafelerinde metre cinsinden kaydırır."""
    lat = float(nokta.get("lat"))
    lon = float(nokta.get("lon"))
    dlat = float(kuzey_m) / 111320.0
    cos_lat = max(abs(math.cos(math.radians(lat))), 1e-6)
    dlon = float(dogu_m) / (111320.0 * cos_lat)

    yeni = dict(nokta)
    yeni["lat"] = lat + dlat
    yeni["lon"] = lon + dlon
    return yeni


def haritadan_turbin_yerlesimi_uret(noktalar, poligon, ruzgar_yonu_deg, grid=None):
    """Harita üzerinden seçilen türbin noktalarını yerleşim kayıtlarına çevirir."""
    if not noktalar or not poligon:
        return [], []

    ileri, _ = latlon_xy_donustur(poligon)
    along_vec, cross_vec = ruzgar_eksenleri(ruzgar_yonu_deg)
    turbinler = []
    uyarilar = []

    for i, nokta in enumerate(noktalar, start=1):
        try:
            lat = float(nokta.get("lat"))
            lon = float(nokta.get("lon"))
        except Exception:
            uyarilar.append(f"T{i} koordinatı okunamadı.")
            continue

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            uyarilar.append(f"T{i} koordinatı geçersiz.")
            continue
        if not nokta_poligon_icinde(lon, lat, poligon):
            uyarilar.append(f"T{i} santral sınırı dışında olduğu için hesaba alınmadı.")
            continue

        x, y = ileri(lon, lat)
        hub_hizi = np.nan
        if grid is not None and not grid.empty and {"lat", "lon", "Hub Rüzgar Hızı (m/s)"}.issubset(grid.columns):
            mesafe2 = (grid["lat"].astype(float) - lat) ** 2 + (grid["lon"].astype(float) - lon) ** 2
            if not mesafe2.empty:
                idx = mesafe2.idxmin()
                try:
                    hub_hizi = float(grid.loc[idx, "Hub Rüzgar Hızı (m/s)"])
                except Exception:
                    hub_hizi = np.nan

        turbinler.append({
            "ad": str(nokta.get("ad") or f"T{len(turbinler) + 1}"),
            "lat": lat,
            "lon": lon,
            "x": float(x),
            "y": float(y),
            "xr": float(np.dot(np.array([x, y], dtype=float), cross_vec)),
            "yr": float(np.dot(np.array([x, y], dtype=float), along_vec)),
            "hub_hizi": float(hub_hizi) if np.isfinite(hub_hizi) else np.nan,
        })

    return turbinler, uyarilar


def manuel_turbin_yerlesimi_uret(koordinat_metni, poligon, ruzgar_yonu_deg, grid=None):
    """Kullanıcının girdiği manuel türbin koordinatlarını yerleşim kayıtlarına çevirir.

    Kabul edilen satırlar:
      39.123456, 37.654321
      T1, 39.123456, 37.654321

    Sıra enlem, boylamdır. Santral sınırı dışındaki noktalar kullanılmaz.
    Hub rüzgâr hızı varsa en yakın rüzgâr-grid hücresinden alınır.
    """
    if not str(koordinat_metni or "").strip() or not poligon:
        return [], []

    ileri, _ = latlon_xy_donustur(poligon)
    along_vec, cross_vec = ruzgar_eksenleri(ruzgar_yonu_deg)
    turbinler = []
    uyarilar = []

    for satir_no, ham in enumerate(str(koordinat_metni).splitlines(), start=1):
        satir = ham.strip()
        if not satir:
            continue
        parc = [p.strip() for p in re.split(r"[;,\t]+", satir) if p.strip()]
        if len(parc) < 2:
            uyarilar.append(f"{satir_no}. satır okunamadı: {satir}")
            continue

        ad = None
        sayisal = parc
        try:
            float(parc[0].replace(",", "."))
        except Exception:
            ad = parc[0]
            sayisal = parc[1:]

        if len(sayisal) < 2:
            uyarilar.append(f"{satir_no}. satırda enlem/boylam eksik.")
            continue

        try:
            lat = float(str(sayisal[0]).replace(",", "."))
            lon = float(str(sayisal[1]).replace(",", "."))
        except Exception:
            uyarilar.append(f"{satir_no}. satırdaki koordinatlar sayısal değil.")
            continue

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            uyarilar.append(f"{satir_no}. satırdaki koordinat aralık dışında.")
            continue
        if not nokta_poligon_icinde(lon, lat, poligon):
            uyarilar.append(f"{ad or f'T{satir_no}'} santral sınırı dışında olduğu için eklenmedi.")
            continue

        x, y = ileri(lon, lat)
        hub_hizi = np.nan
        if grid is not None and not grid.empty and {"lat", "lon", "Hub Rüzgar Hızı (m/s)"}.issubset(grid.columns):
            mesafe2 = (grid["lat"].astype(float) - lat) ** 2 + (grid["lon"].astype(float) - lon) ** 2
            if not mesafe2.empty:
                idx = mesafe2.idxmin()
                try:
                    hub_hizi = float(grid.loc[idx, "Hub Rüzgar Hızı (m/s)"])
                except Exception:
                    hub_hizi = np.nan

        turbinler.append({
            "ad": ad or f"T{len(turbinler) + 1}",
            "lat": float(lat),
            "lon": float(lon),
            "x": float(x),
            "y": float(y),
            "xr": float(np.dot(np.array([x, y], dtype=float), cross_vec)),
            "yr": float(np.dot(np.array([x, y], dtype=float), along_vec)),
            "hub_hizi": float(hub_hizi) if np.isfinite(hub_hizi) else np.nan,
        })

    # Tekrarlanan adları güvenli şekilde T1,T2... olarak düzelt.
    gorulen = set()
    for i, t in enumerate(turbinler, start=1):
        if not t["ad"] or t["ad"] in gorulen:
            t["ad"] = f"T{i}"
        gorulen.add(t["ad"])

    return turbinler, uyarilar


def turbin_elips_cizgileri_uret(turbinler, poligon, rotor_capi_m, ruzgar_yonu_deg,
                                capraz_d=2.5, ruzgar_alti_d=6.0, nokta_sayisi=90):
    """Türbinlerin gerçek 2,5D x 6D yönlü yasak elipslerini harita koordinatlarına dönüştürür."""
    if not turbinler:
        return [], []

    _, geri = latlon_xy_donustur(poligon)
    along_vec, cross_vec = ruzgar_eksenleri(ruzgar_yonu_deg)
    yari_eksen_cross = float(capraz_d) * float(rotor_capi_m)
    yari_eksen_along = float(ruzgar_alti_d) * float(rotor_capi_m)
    acilar = np.linspace(0.0, 2.0 * np.pi, int(nokta_sayisi), endpoint=True)

    tum_lat = []
    tum_lon = []
    for turbin in turbinler:
        merkez = np.array([float(turbin['x']), float(turbin['y'])], dtype=float)
        for aci in acilar:
            nokta = (
                merkez
                + cross_vec * yari_eksen_cross * np.cos(aci)
                + along_vec * yari_eksen_along * np.sin(aci)
            )
            lon, lat = geri(float(nokta[0]), float(nokta[1]))
            tum_lon.append(lon)
            tum_lat.append(lat)
        tum_lon.append(None)
        tum_lat.append(None)
    return tum_lat, tum_lon


def turbin_layout_dataframe(turbinler):
    satirlar = []
    for t in turbinler:
        satir = {
            'Türbin': t['ad'],
            'Enlem': t['lat'],
            'Boylam': t['lon'],
            'Hub Rüzgar Hızı (m/s)': t.get('hub_hizi', np.nan)
        }
        if 'egim' in t:
            satir['Eğim (°)'] = t['egim']
        if 'ti' in t:
            satir['TI'] = t['ti']
        satirlar.append(satir)
    return pd.DataFrame(satirlar)




def surukle_ruzgar_overlay_uret(grid):
    """Manuel editöre sayısal rüzgâr gridini gönderir.

    Google uydu altlığı editörde kalır; rüzgâr renk yüzeyi tarayıcıda doğrudan
    aynı Web-Mercator koordinatlarına çizilir. Böylece PNG/image overlay yükleme
    problemi ortadan kalkar.
    """
    try:
        if grid is None or grid.empty:
            return None

        gerekli = {"lat", "lon", "Hub Rüzgar Hızı (m/s)"}
        if not gerekli.issubset(set(grid.columns)):
            return None

        g = grid[["lat", "lon", "Hub Rüzgar Hızı (m/s)"]].copy()
        g["lat"] = pd.to_numeric(g["lat"], errors="coerce")
        g["lon"] = pd.to_numeric(g["lon"], errors="coerce")
        g["Hub Rüzgar Hızı (m/s)"] = pd.to_numeric(
            g["Hub Rüzgar Hızı (m/s)"], errors="coerce"
        )
        g = g.dropna()
        if g.empty:
            return None

        lonlar = np.sort(g["lon"].unique())
        latlar = np.sort(g["lat"].unique())
        if len(lonlar) < 2 or len(latlar) < 2:
            return None

        mat = (
            g.pivot_table(
                index="lat",
                columns="lon",
                values="Hub Rüzgar Hızı (m/s)",
                aggfunc="mean",
            )
            .reindex(index=latlar, columns=lonlar)
            .to_numpy(dtype=float)
        )

        # Eksikleri doldur.
        dfm = pd.DataFrame(mat)
        dfm = (
            dfm.interpolate(axis=0, limit_direction="both")
               .interpolate(axis=1, limit_direction="both")
               .ffill(axis=0).bfill(axis=0)
               .ffill(axis=1).bfill(axis=1)
        )
        if dfm.isna().all().all():
            return None
        ort = float(np.nanmean(mat))
        mat = dfm.fillna(ort).to_numpy(dtype=float)

        # Tarayıcıya çok büyük matris göndermeyelim; görsel için yeterli örnekleme.
        max_n = 90
        sy = max(1, int(math.ceil(mat.shape[0] / max_n)))
        sx = max(1, int(math.ceil(mat.shape[1] / max_n)))
        mat = mat[::sy, ::sx]
        latlar = latlar[::sy]
        lonlar = lonlar[::sx]

        vmin = float(np.nanpercentile(mat, 1))
        vmax = float(np.nanpercentile(mat, 99))
        if not np.isfinite(vmin) or not np.isfinite(vmax):
            return None
        if vmax <= vmin:
            vmax = vmin + 0.01

        return {
            "matrix": [[float(v) for v in row] for row in mat.tolist()],
            "latitudes": [float(v) for v in latlar.tolist()],
            "longitudes": [float(v) for v in lonlar.tolist()],
            "vmin": vmin,
            "vmax": vmax,
            "bounds": [
                [float(latlar.min()), float(lonlar.min())],
                [float(latlar.max()), float(lonlar.max())],
            ],
        }
    except Exception:
        return None


def suruklenebilir_calisma_karesi(poligon, alan_km, merkez=None, key="wind_square", height=570):
    """Uydu tabanli secici: kareyi surukle, merkez degisince Streamlit'e bildir."""
    from pathlib import Path
    import streamlit.components.v1 as components
    if not poligon:
        return None
    pts = [[float(lon), float(lat)] for lon, lat in poligon]
    if merkez is None:
        # Same initial center as kare_calisma_alani_uret (projected coordinates).
        ileri, geri = latlon_xy_donustur(poligon)
        xy = np.array([ileri(lon, lat) for lon, lat in poligon])
        lon, lat = geri(float(xy[:, 0].mean()), float(xy[:, 1].mean()))
        merkez = [lat, lon]
    folder = Path.home() / ".maki_wind_square_picker_v1"
    folder.mkdir(parents=True, exist_ok=True)
    html_path = folder / "index.html"
    html = r'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    html,body{margin:0;overflow:hidden;font-family:Arial}#map{height:570px;position:relative;overflow:hidden;background:#dce2e6;touch-action:none;cursor:grab}
    #tiles{position:absolute;inset:0;pointer-events:none}img{position:absolute;width:256px;height:256px;pointer-events:none}
    svg{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
    #tip{position:absolute;bottom:6px;left:8px;background:#fffdf2e8;padding:5px 8px;border-radius:6px;font-size:12px;pointer-events:none}
    </style></head><body><div id="map"><div id="tiles"></div><svg id="s" viewBox="0 0 960 570" preserveAspectRatio="none"></svg><div id="tip">Turuncu kareyi sürükle • Bırakınca rüzgâr haritası güncellenir</div></div>
    <script>
    let args={},cx=0,cy=0,zoom=11,drag=null,initialized=false;const W=960,H=570,T=256,svg=document.getElementById('s'),tiles=document.getElementById('tiles');
    function merc(lat,lon){const n=T*2**zoom,p=Math.sin(Math.max(-85,Math.min(85,lat))*Math.PI/180);return [(lon+180)/360*n,(.5-Math.log((1+p)/(1-p))/(4*Math.PI))*n]}
    function unmerc(x,y){const n=T*2**zoom;return [180/Math.PI*(2*Math.atan(Math.exp((.5-y/n)*2*Math.PI))-Math.PI/2),x/n*360-180]}
    function screen(lat,lon){let p=merc(lat,lon);return [p[0]-cx+W/2,p[1]-cy+H/2]}
    function fromscreen(x,y){return unmerc(x+cx-W/2,y+cy-H/2)}
    function draw(){tiles.innerHTML='';const tx0=Math.floor((cx-W/2)/T),tx1=Math.ceil((cx+W/2)/T),ty0=Math.floor((cy-H/2)/T),ty1=Math.ceil((cy+H/2)/T),max=2**zoom;
      for(let x=tx0;x<=tx1;x++)for(let y=ty0;y<=ty1;y++){if(y<0||y>=max)continue;let im=document.createElement('img');im.src=`https://mt1.google.com/vt/lyrs=y&x=${((x%max)+max)%max}&y=${y}&z=${zoom}`;im.style.left=(x*T-cx+W/2)+'px';im.style.top=(y*T-cy+H/2)+'px';tiles.appendChild(im)}
      let poly=(args.polygon||[]).map(p=>screen(p[1],p[0]).join(',')).join(' ');svg.innerHTML=`<polygon points="${poly}" fill="#ff333322" stroke="#ed2929" stroke-width="2"/>`;
      let c=screen(args.center[0],args.center[1]),km=args.km,lat=args.center[0],lon=args.center[1];
      let dlat=km/111.32/2,dlon=km/(111.32*Math.max(.1,Math.cos(lat*Math.PI/180)))/2;
      let nw=screen(lat+dlat,lon-dlon),se=screen(lat-dlat,lon+dlon);
      let rect=document.createElementNS('http://www.w3.org/2000/svg','rect');rect.setAttribute('x',Math.min(nw[0],se[0]));rect.setAttribute('y',Math.min(nw[1],se[1]));rect.setAttribute('width',Math.abs(se[0]-nw[0]));rect.setAttribute('height',Math.abs(se[1]-nw[1]));rect.setAttribute('fill','#ffae0033');rect.setAttribute('stroke','#ff9700');rect.setAttribute('stroke-width','3');rect.setAttribute('style','cursor:move');rect.id='square';svg.appendChild(rect);
      let label=document.createElementNS('http://www.w3.org/2000/svg','text');label.setAttribute('x',c[0]);label.setAttribute('y',c[1]);label.setAttribute('text-anchor','middle');label.setAttribute('fill','#fff');label.setAttribute('stroke','#222');label.setAttribute('paint-order','stroke');label.setAttribute('font-size','13');label.setAttribute('pointer-events','none');label.textContent=`${km} × ${km} km`;svg.appendChild(label);
    }
    svg.addEventListener('pointerdown',e=>{const r=svg.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*W,y=(e.clientY-r.top)/r.height*H;drag={mode:e.target.id==='square'?'square':'pan',x,y,old:args.center.slice(),cx,cy};svg.setPointerCapture(e.pointerId);e.preventDefault()});
    svg.addEventListener('pointermove',e=>{if(!drag)return;const r=svg.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*W,y=(e.clientY-r.top)/r.height*H;
      if(drag.mode==='square'){const old=merc(drag.old[0],drag.old[1]);args.center=unmerc(old[0]+x-drag.x,old[1]+y-drag.y)}else{cx=drag.cx-(x-drag.x);cy=drag.cy-(y-drag.y)}draw()});
    svg.addEventListener('pointerup',e=>{if(!drag)return;const moved=drag.mode==='square'&&(Math.abs(args.center[0]-drag.old[0])+Math.abs(args.center[1]-drag.old[1])>1e-7);drag=null;try{svg.releasePointerCapture(e.pointerId)}catch(_){}if(moved)window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setComponentValue',value:{action:'move',lat:args.center[0],lon:args.center[1]},dataType:'json'},'*')});
    svg.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(5,Math.min(17,zoom+(e.deltaY<0?1:-1)));const p=merc(args.center[0],args.center[1]);cx=p[0];cy=p[1];draw()},{passive:false});
    window.addEventListener('message',e=>{if(e.data?.type!=='streamlit:render')return;let a=e.data.args||{};args={polygon:a.polygon||[],center:a.center||[39,35],km:+a.km||10};if(!initialized){const p=merc(args.center[0],args.center[1]);zoom=Math.max(6,Math.min(14,Math.round(13-Math.log2(args.km/4))));const q=merc(args.center[0],args.center[1]);cx=q[0];cy=q[1];initialized=true}draw();window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',height:570},'*')});
    window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:componentReady',apiVersion:1},'*');
    </script></body></html>'''
    if not html_path.exists() or html_path.read_text(encoding="utf-8") != html:
        html_path.write_text(html, encoding="utf-8")
    component = components.declare_component("maki_square_v1", path=str(folder))
    return component(polygon=pts, center=list(merkez), km=float(alan_km), default=None, key=key)


def suruklenebilir_turbin_haritasi(poligon, turbin_noktalari, add_mode=False, height=570, key="drag_turbine_map", wind_overlay=None):
    """Google uydu + sayısal rüzgâr yüzeyi + sürüklenebilir türbinler."""
    try:
        poligon = poligon or []
        noktalar = turbin_noktalari or []
        if not poligon:
            st.info("Sürükle-bırak düzenleme için önce santral sınırını yükleyin.")
            return None

        plons = [float(p[0]) for p in poligon]
        plats = [float(p[1]) for p in poligon]
        min_lon, max_lon = min(plons), max(plons)
        min_lat, max_lat = min(plats), max(plats)

        if wind_overlay and wind_overlay.get("bounds"):
            wb = wind_overlay["bounds"]
            min_lat = min(min_lat, float(wb[0][0]))
            min_lon = min(min_lon, float(wb[0][1]))
            max_lat = max(max_lat, float(wb[1][0]))
            max_lon = max(max_lon, float(wb[1][1]))

        pad_lon = max((max_lon - min_lon) * 0.16, 0.002)
        pad_lat = max((max_lat - min_lat) * 0.16, 0.002)
        view_bounds = [
            [min_lat - pad_lat, min_lon - pad_lon],
            [max_lat + pad_lat, max_lon + pad_lon],
        ]

        comp_dir = Path.home() / ".maki_wind_google_drag_v3"
        comp_dir.mkdir(parents=True, exist_ok=True)
        html_path = comp_dir / "index.html"

        html_code = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{width:100%;height:100%;margin:0;padding:0;overflow:hidden;background:#dfe5ea;font-family:Inter,"Segoe UI",Arial,sans-serif}
#wrap{position:relative;width:100%;height:570px;overflow:hidden;background:#dfe5ea}
#tiles{position:absolute;inset:0;overflow:hidden}
.tile{position:absolute;width:256px;height:256px;user-select:none;pointer-events:none}
#svg{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
.badge{position:absolute;z-index:20;top:10px;left:50%;transform:translateX(-50%);background:rgba(255,255,255,.96);border:1px solid #d8e2ec;border-radius:10px;padding:7px 12px;font-size:12px;color:#12376d;box-shadow:0 2px 8px rgba(0,0,0,.16);pointer-events:none;white-space:nowrap}
.boundary{fill:none;stroke:#ff3b30;stroke-width:3}
.label{font-size:12px;font-weight:700;fill:#173b70;paint-order:stroke;stroke:white;stroke-width:3px;stroke-linejoin:round}
.turb{cursor:grab;stroke:#fff;stroke-width:3}
.turb:active{cursor:grabbing}
.mapctl{
  position:absolute;z-index:25;right:12px;top:12px;display:flex;flex-direction:column;
  gap:6px
}
.mapctl button{
  width:36px;height:36px;border:1px solid #d7e0e8;border-radius:8px;background:rgba(255,255,255,.96);
  color:#12376d;font-size:20px;font-weight:700;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.16)
}
.mapctl button:hover{background:#fff}
</style>
</head>
<body>
<div id="wrap">
  <div id="tiles"></div>
  <svg id="svg" viewBox="0 0 1000 570" preserveAspectRatio="none"></svg>
  <div id="badge" class="badge">Google uydu + rüzgâr haritası</div>
  <div class="mapctl">
    <button id="zin" title="Yakınlaştır">+</button>
    <button id="zout" title="Uzaklaştır">−</button>
    <button id="zfit" title="Sahaya sığdır">⌂</button>
  </div>
</div>
<script>
const W=1000,H=570,TS=256,NS="http://www.w3.org/2000/svg";
let args={},dragging=null,z=10,originX=0,originY=0;
let panState=null, viewInitialized=false;
const tiles=document.getElementById("tiles"),svg=document.getElementById("svg");

function sendValue(value){
  window.parent.postMessage({isStreamlitMessage:true,type:"streamlit:setComponentValue",value:value,dataType:"json"},"*");
}
function setHeight(){
  window.parent.postMessage({isStreamlitMessage:true,type:"streamlit:setFrameHeight",height:570},"*");
}
function clampLat(lat){return Math.max(-85.05112878,Math.min(85.05112878,lat));}
function worldXY(lat,lon,zoom){
  lat=clampLat(lat);
  const n=Math.pow(2,zoom)*TS;
  const x=(lon+180)/360*n;
  const s=Math.sin(lat*Math.PI/180);
  const y=(0.5-Math.log((1+s)/(1-s))/(4*Math.PI))*n;
  return {x,y};
}
function screenXY(lat,lon){
  const p=worldXY(lat,lon,z);
  return{x:(p.x-originX)/W*1000,y:(p.y-originY)/H*570};
}
function screenToLL(svgX,svgY){
  const px=svgX/1000*W,py=svgY/570*H;
  const n=Math.pow(2,z)*TS;
  const wx=px+originX,wy=py+originY;
  const lon=wx/n*360-180;
  const yy=0.5-wy/n;
  const lat=90-360*Math.atan(Math.exp(-yy*2*Math.PI))/Math.PI;
  return{lat,lon};
}
function chooseView(){
  const b=args.view_bounds;
  const sw={lat:+b[0][0],lon:+b[0][1]},ne={lat:+b[1][0],lon:+b[1][1]};
  let chosen=6;
  for(let zz=6;zz<=18;zz++){
    const p1=worldXY(sw.lat,sw.lon,zz),p2=worldXY(ne.lat,ne.lon,zz);
    const ww=Math.abs(p2.x-p1.x),hh=Math.abs(p1.y-p2.y);
    if(ww<=W*.88&&hh<=H*.88)chosen=zz;else break;
  }
  z=chosen;
  const pSW=worldXY(sw.lat,sw.lon,z),pNE=worldXY(ne.lat,ne.lon,z);
  const minX=Math.min(pSW.x,pNE.x),maxX=Math.max(pSW.x,pNE.x);
  const minY=Math.min(pSW.y,pNE.y),maxY=Math.max(pSW.y,pNE.y);
  originX=(minX+maxX)/2-W/2;
  originY=(minY+maxY)/2-H/2;
}

function redrawMap(){
  drawTiles();
  drawSvg();
}
function zoomAt(newZ, clientX, clientY){
  newZ=Math.max(6,Math.min(20,newZ));
  if(newZ===z)return;

  const r=svg.getBoundingClientRect();
  const px=((clientX-r.left)/r.width)*W;
  const py=((clientY-r.top)/r.height)*H;

  const before=screenToLL(px/W*1000,py/H*570);
  z=newZ;
  const world=worldXY(before.lat,before.lon,z);
  originX=world.x-px;
  originY=world.y-py;
  redrawMap();
}
function zoomCenter(delta){
  const r=svg.getBoundingClientRect();
  zoomAt(z+delta,r.left+r.width/2,r.top+r.height/2);
}
function fitView(){
  chooseView();
  redrawMap();
}

function drawTiles(){
  tiles.innerHTML="";
  const x0=Math.floor(originX/TS)-1,x1=Math.floor((originX+W)/TS)+1;
  const y0=Math.floor(originY/TS)-1,y1=Math.floor((originY+H)/TS)+1;
  const maxTile=Math.pow(2,z);
  for(let tx=x0;tx<=x1;tx++){
    for(let ty=y0;ty<=y1;ty++){
      if(ty<0||ty>=maxTile)continue;
      const wrapX=((tx%maxTile)+maxTile)%maxTile;
      const img=document.createElement("img");
      img.className="tile";
      img.src=`https://mt1.google.com/vt/lyrs=y&x=${wrapX}&y=${ty}&z=${z}`;
      img.style.left=(tx*TS-originX)+"px";
      img.style.top=(ty*TS-originY)+"px";
      tiles.appendChild(img);
    }
  }
}
function el(name,attrs={}){
  const e=document.createElementNS(NS,name);
  for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);
  return e;
}
function clearSvg(){while(svg.firstChild)svg.removeChild(svg.firstChild);}
function colorFor(v,vmin,vmax){
  let t=(v-vmin)/Math.max(vmax-vmin,1e-9);
  t=Math.max(0,Math.min(1,t));
  const stops=[
    [0.00,[85,39,207]],[0.12,[39,56,232]],[0.28,[23,141,242]],
    [0.43,[34,215,237]],[0.57,[85,231,190]],[0.70,[53,223,98]],
    [0.84,[186,242,56]],[0.94,[255,240,68]],[1.00,[255,159,36]]
  ];
  for(let i=1;i<stops.length;i++){
    if(t<=stops[i][0]){
      const a=stops[i-1],b=stops[i],q=(t-a[0])/(b[0]-a[0]);
      const c=a[1].map((x,j)=>Math.round(x+(b[1][j]-x)*q));
      return`rgb(${c[0]},${c[1]},${c[2]})`;
    }
  }
  return"rgb(255,159,36)";
}
function drawWind(){
  const w=args.wind;
  if(!w||!w.matrix||!w.latitudes||!w.longitudes)return;

  const M=w.matrix,lats=w.latitudes,lons=w.longitudes;
  const ny=M.length,nx=(M[0]||[]).length;
  if(!ny||!nx)return;

  const dlat=lats.length>1?Math.abs(+lats[1]-+lats[0]):0.001;
  const dlon=lons.length>1?Math.abs(+lons[1]-+lons[0]):0.001;
  const grp=el("g",{opacity:"0.76","pointer-events":"none"});

  for(let iy=0;iy<ny;iy++){
    for(let ix=0;ix<nx;ix++){
      const lat=+lats[iy],lon=+lons[ix],v=+M[iy][ix];
      const nw=screenXY(lat+dlat/2,lon-dlon/2);
      const se=screenXY(lat-dlat/2,lon+dlon/2);
      grp.appendChild(el("rect",{
        x:Math.min(nw.x,se.x),
        y:Math.min(nw.y,se.y),
        width:Math.max(1,Math.abs(se.x-nw.x)+.8),
        height:Math.max(1,Math.abs(se.y-nw.y)+.8),
        fill:colorFor(v,+w.vmin,+w.vmax),
        stroke:"none"
      }));
    }
  }
  svg.appendChild(grp);
}
function insidePolygon(lat,lon){
  const poly=args.polygon||[];let x=lon,y=lat,inside=false;
  for(let i=0,j=poly.length-1;i<poly.length;j=i++){
    const xi=+poly[i][0],yi=+poly[i][1],xj=+poly[j][0],yj=+poly[j][1];
    const hit=((yi>y)!=(yj>y))&&(x<(xj-xi)*(y-yi)/((yj-yi)||1e-15)+xi);
    if(hit)inside=!inside;
  }
  return inside;
}
function payload(){
  return(args.points||[]).map((p,i)=>({
    lat:+p.lat,lon:+p.lon,ad:p.ad||("T"+(i+1)),
    excel_lat:p.excel_lat??null,excel_lon:p.excel_lon??null
  }));
}
function drawSvg(){
  clearSvg();
  drawWind();

  const poly=args.polygon||[];
  if(poly.length){
    const pts=poly.map(p=>{
      const q=screenXY(+p[1],+p[0]);
      return q.x+","+q.y;
    }).join(" ");
    svg.appendChild(el("polygon",{points:pts,class:"boundary"}));
  }

  (args.points||[]).forEach((p,i)=>{
    const q=screenXY(+p.lat,+p.lon),g=el("g",{"data-i":i});
    const c=el("circle",{cx:q.x,cy:q.y,r:12,fill:"#ff6b6b",class:"turb"});
    const t=el("text",{x:q.x,y:q.y-17,"text-anchor":"middle",class:"label"});
    t.textContent=p.ad||("T"+(i+1));

    c.addEventListener("pointerdown",ev=>{
      ev.preventDefault();ev.stopPropagation();
      dragging={i,c,t,startLat:+p.lat,startLon:+p.lon};
      c.setPointerCapture(ev.pointerId);
    });
    c.addEventListener("pointermove",ev=>{
      if(!dragging||dragging.i!==i)return;
      const r=svg.getBoundingClientRect();
      const x=(ev.clientX-r.left)/r.width*1000;
      const y=(ev.clientY-r.top)/r.height*570;
      c.setAttribute("cx",x);c.setAttribute("cy",y);
      t.setAttribute("x",x);t.setAttribute("y",y-17);
    });
    c.addEventListener("pointerup",ev=>{
      if(!dragging||dragging.i!==i)return;
      const ll=screenToLL(+c.getAttribute("cx"),+c.getAttribute("cy"));
      if(insidePolygon(ll.lat,ll.lon)){
        args.points[i].lat=ll.lat;args.points[i].lon=ll.lon;
        sendValue({action:"update",points:payload()});
      }else{
        args.points[i].lat=dragging.startLat;
        args.points[i].lon=dragging.startLon;
        drawSvg();
      }
      dragging=null;
    });
    g.appendChild(c);g.appendChild(t);svg.appendChild(g);
  });
}
function render(){
  if(!viewInitialized){
    chooseView();
    viewInitialized=true;
  }
  drawTiles();
  drawSvg();
  document.getElementById("badge").textContent=args.add_mode
    ?"Ekleme modu açık · Google uydu + rüzgâr alanında boş noktaya tıklayın"
    :"Google uydu + rüzgâr haritası · Türbini sürükleyin";
}

document.getElementById("zin").addEventListener("click",ev=>{
  ev.preventDefault();ev.stopPropagation();zoomCenter(1);
});
document.getElementById("zout").addEventListener("click",ev=>{
  ev.preventDefault();ev.stopPropagation();zoomCenter(-1);
});
document.getElementById("zfit").addEventListener("click",ev=>{
  ev.preventDefault();ev.stopPropagation();fitView();
});

svg.addEventListener("wheel",ev=>{
  ev.preventDefault();
  const delta=ev.deltaY<0?1:-1;
  zoomAt(z+delta,ev.clientX,ev.clientY);
},{passive:false});

svg.addEventListener("pointerdown",ev=>{
  // Türbin sürükleme kendi event'inde yönetilir.
  if(ev.target&&ev.target.classList&&ev.target.classList.contains("turb"))return;
  // Ekleme modu açıkken tek tıklama yeni türbin eklemek için ayrılır.
  if(args.add_mode)return;
  panState={x:ev.clientX,y:ev.clientY,ox:originX,oy:originY,moved:false};
  svg.setPointerCapture(ev.pointerId);
});
svg.addEventListener("pointermove",ev=>{
  if(!panState)return;
  const r=svg.getBoundingClientRect();
  const dx=(ev.clientX-panState.x)/r.width*W;
  const dy=(ev.clientY-panState.y)/r.height*H;
  if(Math.abs(dx)>2||Math.abs(dy)>2)panState.moved=true;
  originX=panState.ox-dx;
  originY=panState.oy-dy;
  redrawMap();
});
svg.addEventListener("pointerup",ev=>{
  if(!panState)return;
  panState=null;
  try{svg.releasePointerCapture(ev.pointerId);}catch(e){}
});

svg.addEventListener("click",ev=>{
  if(!args.add_mode||dragging)return;
  if(ev.target&&ev.target.classList&&ev.target.classList.contains("turb"))return;
  const r=svg.getBoundingClientRect();
  const x=(ev.clientX-r.left)/r.width*1000;
  const y=(ev.clientY-r.top)/r.height*570;
  const ll=screenToLL(x,y);
  if(!insidePolygon(ll.lat,ll.lon))return;
  const i=(args.points||[]).length;
  args.points.push({
    lat:ll.lat,lon:ll.lon,ad:"T"+(i+1),
    excel_lat:null,excel_lon:null
  });
  drawSvg();
  sendValue({action:"update",points:payload()});
});
window.addEventListener("message",event=>{
  if(!event.data||event.data.type!=="streamlit:render")return;
  const a=event.data.args||{};
  const oldBounds=JSON.stringify(args.view_bounds||null);
  const newBounds=JSON.stringify(a.view_bounds||null);
  args={
    polygon:a.polygon||[],
    points:(a.points||[]).map(p=>Object.assign({},p)),
    add_mode:!!a.add_mode,
    view_bounds:a.view_bounds,
    wind:a.wind||null
  };
  if(oldBounds!==newBounds)viewInitialized=false;
  render();setHeight();
});
window.parent.postMessage({
  isStreamlitMessage:true,
  type:"streamlit:componentReady",
  apiVersion:1
},"*");
setHeight();
</script>
</body>
</html>"""

        if (not html_path.exists()) or html_path.read_text(encoding="utf-8") != html_code:
            html_path.write_text(html_code, encoding="utf-8")

        component = components.declare_component(
            f"maki_google_drag_v3_{key}",
            path=str(comp_dir),
        )

        return component(
            polygon=[[float(lon), float(lat)] for lon, lat in poligon],
            points=[
                {
                    "lat": float(p.get("lat")),
                    "lon": float(p.get("lon")),
                    "ad": str(p.get("ad") or f"T{i+1}"),
                    "excel_lat": p.get("excel_lat"),
                    "excel_lon": p.get("excel_lon"),
                }
                for i, p in enumerate(noktalar)
            ],
            add_mode=bool(add_mode),
            view_bounds=view_bounds,
            wind=wind_overlay,
            default=None,
            key=key,
        )
    except Exception as hata:
        st.warning(f"Sürükle-bırak türbin editörü açılamadı: {hata}")
        return {"action": "editor_error", "error": str(hata)}


# ============================================================
# SOL MENÜ — MAKI WIND STUDIO V8
# ============================================================

st.sidebar.markdown(
    f"""
    <div class="sidebar-brand v8-brand">
        <div class="sidebar-logo-wrap">
            <img class="sidebar-logo" src="{MAKI_LOGO_DATA_URI}" alt="Maki Enerji">
        </div>
        <div class="v8-product-name">MAKI WIND STUDIO</div>
        <span class="sub">RÜZGÂR ÖLÇÜM · MICROSITING · AEP</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Menü seçimi butonlarla yönetilir. Bu yöntem CSS hover menülerinden daha sağlamdır
# ve alt modüllerin her ekran çözünürlüğünde okunur kalmasını sağlar.
V8_SAYFALAR = {
    "Ana Sayfa": "Ana Sayfa",
    "Veri Yükleme ve Direk Ayarları": "Rüzgar Ölçümleri",
    "Rüzgar Kaynağı Özeti": "Rüzgar Kaynağı Özeti",
    "Veri İnceleme": "Veri İnceleme",
    "Yüksek Çözünürlüklü Topografya": "Topografya Modülü",
    "Micrositing ve AEP": "Üretim Hesaplama",
    "Kılavuz": "Kılavuz",
}

if "aktif_sayfa_v8" not in st.session_state:
    kayitli_sayfa = str(app_state.get("active_page", "Ana Sayfa") or "Ana Sayfa")
    eski_sayfa = st.session_state.get("ana_navigasyon", kayitli_sayfa)
    st.session_state["aktif_sayfa_v8"] = eski_sayfa if eski_sayfa in V8_SAYFALAR.values() else "Ana Sayfa"


def navigasyona_git(hedef):
    st.session_state["aktif_sayfa_v8"] = hedef
    app_state["active_page"] = hedef


def ana_sayfadan_veri_yuklemeye_git():
    st.session_state["ruzgar_olcumleri_adim_v112"] = 1
    app_state["measurement_step"] = 1
    navigasyona_git("Rüzgar Ölçümleri")


def v8_menu_butonu(etiket, hedef, ikon="", alt=False):
    """Ek HTML sarmalayıcı üretmeden kompakt sidebar düğmesi oluşturur."""
    aktif = st.session_state.get("aktif_sayfa_v8") == hedef
    alt_isareti = "↳ " if alt else ""
    gorunen_ikon = "" if alt else ikon
    tiklandi = st.sidebar.button(
        f"{alt_isareti}{gorunen_ikon}  {etiket}",
        key=f"v8_nav_{hedef}",
        use_container_width=True,
        type="primary" if aktif else "secondary",
    )
    if tiklandi:
        navigasyona_git(hedef)
        st.rerun()


st.sidebar.markdown('<div class="v8-menu-caption">GENEL</div>', unsafe_allow_html=True)
v8_menu_butonu("Ana Sayfa", "Ana Sayfa", "⌂")

st.sidebar.markdown('<div class="v8-menu-caption">RÜZGÂR ÖLÇÜMLERİ</div>', unsafe_allow_html=True)
v8_menu_butonu("Veri Yükleme ve Direk Ayarları", "Rüzgar Ölçümleri", "⇧")
v8_menu_butonu("Rüzgar Kaynağı Özeti", "Rüzgar Kaynağı Özeti", "", alt=True)

st.sidebar.markdown('<div class="v8-menu-caption">VERİ İŞLEME</div>', unsafe_allow_html=True)
v8_menu_butonu("Veri İnceleme", "Veri İnceleme", "〽")

st.sidebar.markdown('<div class="v8-menu-caption">PROJE GELİŞTİRME</div>', unsafe_allow_html=True)
v8_menu_butonu("Micrositing ve AEP", "Üretim Hesaplama", "△")
v8_menu_butonu("Kılavuz", "Kılavuz", "☰")

if st.session_state["aktif_sayfa_v8"] == "Çoklu Veri Karşılaştırma":
    navigasyona_git("Rüzgar Kaynağı Özeti")
if st.session_state["aktif_sayfa_v8"] in {"Ham Rüzgar Hızları", "Temizlenmiş Rüzgar Hızları"}:
    navigasyona_git("Veri İnceleme")
sayfa = st.session_state["aktif_sayfa_v8"]
app_state["active_page"] = sayfa

_BULUT_PROJE_HAZIR = True
try:
    bulut_proje_verisini_al()
    st.session_state.pop('_bulut_hata', None)
except Exception as _cloud_error:
    st.session_state['_bulut_hata'] = str(_cloud_error)
if st.session_state.get('_bulut_hata'):
    st.warning('Bulut proje verisi alınamadı; son çalışma verisi korundu. ' + st.session_state['_bulut_hata'])
if st.session_state.get('_bulut_ayar_uyarisi'):
    st.warning(st.session_state.pop('_bulut_ayar_uyarisi'))
bulut_proje_canli_durumu()

# Keep one component at a stable main-page position so active transfers survive navigation.
with st.expander("LoggerNet otomatik bağlantı", expanded=(sayfa == "Rüzgar Ölçümleri")):
    st.caption("Chrome’da bir kez klasörü bağlayın. Proje bağlantısını kopyalayıp sohbetin sağındaki panelde açın; panel buluttaki verileri klasör izni istemeden kullanır. Yeni yerel ölçümler için Chrome sekmesi açık kalmalıdır.")
    if app_state.get("data_source") == "Manuel dosya yükleme":
        st.info("Mevcut manuel veriyi korumak için otomatik klasörü boş bir proje sekmesinde bağlayın.")
    tarayici_loggernet_paneli()
if st.session_state.get('_bulut_hata') and app_state.get('data_source') == 'Tarayıcı LoggerNet klasörü':
    st.info('Buluttaki ölçümler doğrulanamadığı için analiz bekletiliyor. İzin verdiğiniz Chrome sekmesi açıkken dosyalar yeniden alınabilir.')
    st.stop()

# ============================================================
# LOGGERNET OTOMATİK SENKRONİZASYONU
# ============================================================
# LoggerNet her gün 11:00'de WindData dosyalarını güncelliyor. Uygulama her
# Streamlit çalışmasında klasörü hafif bir metadata taramasıyla kontrol eder.
# Dosya değişmişse cache anahtarları (mtime/size) yenilenir ve analiz sayfaları
# en güncel veriyi kendiliğinden kullanır.
_loggernet_klasoru = app_state.get("loggernet_folder", r"C:\Campbellsci\veriler")
_loggernet_sync = loggernet_otomatik_senkronize(
    _loggernet_klasoru, app_state.get("wind_data_files", [])
)
if app_state.get("data_source") not in {"Manuel dosya yükleme", "Tarayıcı LoggerNet klasörü"} and _loggernet_sync["files"]:
    if _loggernet_sync["changed"]:
        app_state["wind_data_files"] = _loggernet_sync["files"]
        app_state["loggernet_new_files"] = _loggernet_sync["new_files"]
        app_state["loggernet_changed_files"] = _loggernet_sync["changed_files"]
    app_state["data_source"] = "LoggerNet klasörü"
    app_state["loggernet_last_scan"] = datetime.datetime.now().isoformat(timespec="seconds")
    if _loggernet_sync["last_data_update"] is not None:
        app_state["loggernet_last_data_update"] = _loggernet_sync["last_data_update"].isoformat(timespec="seconds")

# Oturum durumu — app_state üzerinden hafifçe hesaplanır, dosyalar burada okunmaz.
_v8_dosya_sayisi = len(app_state.get("wind_data_files", []))
_v8_sinir_var = bool(app_state.get("santral_boundary"))
_v8_turbin_modeli = app_state.get("turbine_model") or "Seçilmedi"
_v8_sistem = "HAZIR" if _v8_dosya_sayisi else "VERİ BEKLİYOR"

st.sidebar.markdown(
    f"""
    <div class="v8-status-panel">
        <div class="v8-status-title">OTURUM DURUMU</div>
        <div class="v8-status-item"><span class="v8-dot {'ok' if _v8_dosya_sayisi else 'wait'}"></span><b>{_v8_sistem}</b></div>
        <div class="v8-status-grid">
            <div><span>Wind data</span><b>{_v8_dosya_sayisi}</b></div>
            <div><span>Santral sınırı</span><b>{'Yüklü' if _v8_sinir_var else 'Yok'}</b></div>
        </div>
        <div class="v8-status-model"><span>Türbin modeli</span><b>{_v8_turbin_modeli}</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.caption("Yüklemeler ve ayarlar bu tarayıcı oturumu boyunca korunur.")
st.sidebar.markdown("---")

# Yüklenen dosyalar widget değerleri olarak değil, byte tabanlı kayıtlar
# şeklinde oturumda tutulur. Ana sayfa veri okumadan hızlı açılır.
dosyalar = [
    kayitli_dosyayi_olustur(kayit)
    for kayit in app_state.get("wind_data_files", [])
    if kayit
]

# ============================================================
# VERİDEN BAĞIMSIZ GİRİŞ EKRANI
# ============================================================
if sayfa == "Kılavuz":
    st.markdown("## Kılavuz")
    st.caption("Maki Wind Studio · v11.11.24 · Ölçümden enerji tahminine adım adım")
    st.write("Bu program rüzgâr ölçümlerini inceler, sorunlu ölçümleri ayırmaya yardımcı olur, saha ve türbin yerleşimi üzerinde çalışmanızı sağlar ve geçerli ölçümlerden güç eğrisiyle enerji tahmini hesaplar.")
    st.info("Önerilen sıra: Veri Yükleme ve Direk Ayarları → Rüzgar Kaynağı Özeti → Veri İnceleme → Micrositing ve AEP. Bu kılavuz veri yüklemeden de açılır.")

    with st.expander("1 · Ölçüm dosyalarını yükleyin", expanded=True):
        st.markdown("""
**Veri Yükleme ve Direk Ayarları** sayfasından veri kaynağını seçin.
- **LoggerNet klasörü:** Uygulamanın çalıştığı bilgisayardaki WindData dosyaları taranır; dosya değişiklikleri uygulama yeniden çalıştığında kontrol edilir. Klasör yolunu kendi kurulumunuza göre girin. Bulutta çalışan uygulama, Windows bilgisayarınızdaki klasöre doğrudan erişemez.
- **Manuel dosya yükleme:** TOA5 veya uyumlu CSV dosyanızı seçin. Okuyucu zaman sütununu ve WS1_Avg benzeri hız kanallarını arar. Farklı sütun şemaları ayrıca eşleştirme gerektirebilir.
- Birden fazla direği ayrı veri setleri olarak yükleyin. Aynı adlı dosyaları ve direkleri karıştırmayın; dosya adı sensör yüksekliği veya arıza kanıtı değildir.

**Bulutta otomatik klasör bağlantısı ve ortak proje:** Chrome’da klasör bağlandıktan sonra **Proje bağlantısını kopyala** ile alınan adresi sohbetin sağındaki tarayıcıda açın. İki tarayıcı aynı proje verisini kullanır; panelde yerel klasör izni gerekmez. Sensör yükseklikleri, direk kayıtları, koordinatlar ve kalite işaretleri proje kapsamında eşitlenir. Ekran ve tarih seçimleri tarayıcıya özeldir. Bağlantıya sahip olanlar verilere erişebilir; yalnızca yetkili kişilerle paylaşın. Bu aktarım deposu sunucu diskindedir, kalıcı yedek değildir; sunucu yeniden kurulursa Chrome verileri yeniden aktarmalıdır.

**Yerel klasörü bağlama:** Sayfanın üstündeki **LoggerNet otomatik bağlantı** bölümünde **Klasörü bağla / izni yenile** düğmesine basıp kendi Windows klasörünüzü seçin. Tarayıcı yalnızca okuma izni ister; dosyalar analiz için buluta aktarılır. Uyumlu Chrome/Edge, açık sekme ve internet gerekir. Tarama 15 saniyede birdir; arka plan kısıtları veya uyku takip aralığını uzatabilir. Tarayıcı izin desteklemiyorsa bağlantı kurulmuş sayılmaz. Farklı klasörü/direk grubunu yeni proje sekmesinde bağlayın. Her dosya en fazla 64 MB olabilir; yarım yazılmış veya bozuk aktarım son veriyi değiştirmez. Klasörden silinen dosya çalışma setinden otomatik silinmez; panelde uyarılır.

**Kontrol edin:** Doğru dosya, doğru direk, başlangıç/bitiş tarihleri ve yeni dosyanın gerçekten yüklendiği.
""")
    with st.expander("2 · Direk ve sensör bilgilerini doğrulayın"):
        st.markdown("""
Kurulum raporu varsa yükleyin; algılanan bilgileri onaylamadan önce raporla karşılaştırın. Direk koordinatlarını ve her hız/yön sensörünün yüksekliğini doğru girin.

TOA5 dosyasının hız kanalı adı tek başına sensör yüksekliğini belirtmez. Bir direğin yüksekliklerini başka direğe taşımayın. Yüksekliği bilinmeyen ölçümü göbek yüksekliğine dönüştürmeyin.

**Kontrol edin:** Hangi kanalın hangi sensöre ait olduğu, ölçüm yüksekliği, rapor ve veri seti eşleştirmesi. Bazı mevcut ekranlar ve enerjiye aktarım WS1–WS4 kanalları üzerine kuruludur; her dosya şemasının desteklendiği varsayılmamalıdır.
""")
    with st.expander("3 · Veri setini ve tarih aralığını seçin; istatistikleri okuyun"):
        st.markdown("""
**Rüzgar Kaynağı Özeti** sayfasında bir veri seti ve tarih aralığı seçin. Ham veya temizlenmiş görünümü seçerek aylık ortalama, medyan, minimum, maksimum ve standart sapmayı inceleyin. Grafikler bölümünü açarak zaman serilerini, hız/yön dağılımlarını ve yükseklik profilini değerlendirin.

Ortalama genel düzeyi, medyan ortadaki ölçümü, standart sapma ise değişkenliği gösterir. Minimum ve maksimum değerler ayrıca incelenmelidir. Seçilen veri ve dönem istatistikleri etkiler.

**Önemli:** Eksik ölçümleri olan bir ayın ortalaması yalnızca kalan geçerli ölçümlerin ortalamasıdır; bütün ayın temsil edildiğini göstermez. Aylık tabloyu veri kapsamı raporuyla birlikte okuyun.
""")
    with st.expander("4 · Ham, gerçek temiz ve tahmini veriyi ayırın"):
        st.markdown("""
- **Ham veri:** Dosyadan okunan ölçümler korunur; sorunlu sensör değerleri de bulunabilir. Orijinal yüklenen dosya değiştirilmez.
- **Gerçek temiz ölçüm:** Fiziksel aralık kontrolleri, otomatik olaylar ve manuel kalite işaretlerinden sonra kalan gerçek ölçümlerdir. Dışlanan değer boş bırakılır; mevcut zaman satırı korunur. Dosyada hiç bulunmayan zamanlar kapsam hesabında eksik sayılır.
- **Tahmini aday:** Aynı direğin diğer sağlam ölçümlerinden modellenen tamamlama adayıdır. Kaynak sütunuyla ayrılır, ayrı CSV'ye çıkarılır ve aktif enerji hesabına dahil edilmez.

Örnek: 100 ölçümün 10'u dışlanırsa 90 gerçek ölçüm ve 10 boş değer kalır. Ortalama 90 ölçümden hesaplanır. Tahmin eklense bile tahmini kayıt gerçek ölçüme dönüşmez.

**Ham Veri** görünümünü seçmek enerji hesabını ham veriye geçirmez. Temizlenmiş etiketi, kalan ölçümlerin bağımsız olarak doğrulandığı anlamına gelmez.
""")
    with st.expander("5 · Kalite işaretlerini ve zaman eksenini inceleyin"):
        st.markdown("""
**Yüklenen bütün dosyaların ön kontrol özeti** ile **Veri kalitesi ve enerjiye uygunluk raporu** bölümlerini açın.
- Sayısal olmayan/sonsuz ve 0–45 m/s dışındaki hızlar temiz ölçümden dışlanır. Bu aralık uygulama tercihidir; bütün cihazlar için doğrulanmış fiziksel sınır değildir.
- Uzun sıfıra yakın veya sabit ölçüm, süre ve en az iki başka sensörden destek koşullarıyla işaretlenebilir. Tek sıfır, kısa sıfır dizisi veya bütün sensörlerin birlikte sakin olması tek başına dışlama nedeni değildir.
- İki destek sensörü yoksa bu çapraz kontrol çalışmaz. Ani sıçrama, buzlanma, kalibrasyon değişimi ve direk gölgelemesi gibi sorunlar ayrıca incelenmelidir.
- Yinelenen/geçersiz zamanları, kayıt aralığını, beklenen ve geçerli kayıt sayılarını, aylık kapsamı ve en uzun boşluğu kontrol edin.

Gerekirse **Sorunlu ölçümleri işaretle** bölümünde sensör ve zaman aralığı seçin. Geri alma işlemi mevcut sürümde seçili sensörün tüm manuel işaretlerini kaldırır; ayrıntılı işlem geçmişi değildir. **Veri İnceleme** sayfasında ham/temiz tabloyu karşılaştırıp CSV indirebilirsiniz.

Otomatik işaret arıza teşhisi değildir. Üst sensörün alt sensörden düşük ölçmesi tek başına hata değildir; gerçek sakinliği silmeyin. Windographer karşılaştırmasını aynı dönem, sensör, zaman dilimi, filtreler ve geçerli kayıt sayılarıyla yapın.
""")
    with st.expander("6 · Eksik veri tamamlama yöntemini sınayın"):
        st.markdown("""
**Eksik veri tamamlama · yöntem testi** bölümünde hedef sensörü, aynı direkteki sağlam referansı, test boşluğu uzunluğunu ve test güç eğrisini seçin. **Sağlam dönemlerde yöntemi test et** düğmesine basın.

Model hedef hızı referans hızından doğrusal ilişkiyle tahmin eder. Ardışık test blokları eğitimden çıkarılır; iki tarafta yedişer günlük tampon kullanılır. Yeterli ortak ölçüm ve test bloğu yoksa model verilmez. İlişki katsayıları her direğin kendi verisinden hesaplanır.

Ortalama hız sapması, MAE (ortalama mutlak hata), RMSE (büyük hatalara daha duyarlı hata ölçüsü) ve güç eğrisi enerji sapmasını birlikte okuyun. Eğitimde 0,25 m/s üzerindeki ortak ölçümler kullanılır; düşük hızlara etkisi ayrıca değerlendirilmelidir. Adaylar referansın eğitim aralığı dışında üretilmez.

Güç eğrisi testi hedef sensör yüksekliğindedir; göbek dönüşümünü veya hava yoğunluğunu doğrulamaz. İyi test sonucu, gerçek eksik dönemin doğru tamamlandığını kanıtlamaz. Mevsim/yön etkisi, referans kalitesi ve tahmin belirsizliği ayrıca değerlendirilmelidir. Aday CSV aktif enerji girdisi değildir.
""")
    with st.expander("7 · Doğrudan Micrositing ve AEP sayfasına geçin"):
        st.markdown("""
Sol menüden **Micrositing ve AEP** sayfasını doğrudan açabilirsiniz. Veri kalitesi sayfasını ziyaret etmek veya ayrıca inceleme onayı vermek zorunlu değildir. Rüzgar Kaynağı Özeti sayfasındaki **Enerji hesabına geç** düğmesi de aynı sayfayı açar.

Sayfaya erişim, enerji hesabının yapılabildiği anlamına gelmez. Hesap gerçek temiz ölçümleri kullanır; kalite işaretleri otomatik uygulanır. Geçersiz zaman ekseni, eksik sensör yüksekliği veya hesaplanamayan göbek dönüşümü hesaplamayı engelleyebilir. Yetersiz yıllık kapsamda yıllık sonuç gösterilmez. Bu teknik kontroller kullanıcı onayı değildir.

Kalite işaretleri yerel proje sekmesi kapsamında saklanır; bütün tarayıcı sekmelerinde ortak proje veritabanı değildir. Önemli raporları ve CSV çıktılarını ayrıca saklayın. Önceki sürümlerdeki inceleme kayıtları yeni sürümde enerjiye erişim şartı olarak kullanılmaz.
""")
    with st.expander("8 · Türbini seçin; güç ve enerji hesabını okuyun"):
        st.markdown("""
**Micrositing ve AEP** sayfasında ilgili ölçüm verisini, türbin modelini, göbek yüksekliğini, türbin adedini ve kayıp senaryosunu kontrol edin. İsteğe bağlı topografya adımı görünüyorsa yalnızca elinizdeki doğrulanmış kaynaklarla ilerleyin.

Enerji hesabının sırası:
1. Gerçek temiz referans ölçümleri alınır.
2. Farklı yüksekliğe dönüşüm gerekiyorsa ölçümlerden hesaplanan shear (yükseklikle hız değişimi) kullanılır. En az iki farklı geçerli yükseklik ve 30 ortak kayıt gerekir. Hesaplanamıyorsa sessizce sabit alpha kullanılmaz; aynı ölçüm yüksekliğinde dönüşüm gerekmez.
3. Her geçerli zamandaki göbek hızı, seçili türbinin gömülü güç eğrisinde güce çevrilir. Birden fazla direk kullanılırsa o zamandaki mevcut göbek hızlarının ortalaması alınır; bu işlem tek başına doğrulanmış mekânsal akış modeli değildir.
4. Güç (kW) × özgün kayıt süresi (saat) = enerji (kWh). Türbin adedi uygulanır. Eksik kayıtlar süreyi büyütmez ve tahminle doldurulmaz.
5. Wake, kullanılabilirlik, elektrik ve diğer tanımlı kayıplar çarpan olarak uygulanır. Örneğin %10 ve %5 kayıp birlikte 0,90 × 0,95 çarpanıdır.

**Geçerli kayıtlardan net enerji tahmini**, yalnızca hesaplanan kayıtlara aittir; boşluklar dahil bütün dönem üretimi değildir. Ölçülmüş elektrik üretimi de değildir. Birden fazla direğin farklı kayıt aralıklarıyla birleştirilmesi ayrıca doğrulanmalıdır. Güç eğrisinin modeli, nominal gücü ve hava yoğunluğu koşulları özgün belgelerle teyit edilmelidir.
""")
    with st.expander("9 · Yıllık Net Üretim ve kapasite faktörünü doğru yorumlayın"):
        st.markdown("""
Yıllık ön tahmin için mevcut uygulamanın koşulları birlikte sağlanmalıdır:
- En az 365 günlük zaman aralığı.
- Seçilen aralıktaki her yıl-ay için en az %90 geçerli gerçek referans ölçümü.
- En uzun tek eksik/dışlanan aralık en fazla 2 saat.
- Uygun zaman ekseni; çoklu direkte kullanılan her direğin kapsam koşullarını sağlaması.

Koşullar sağlanmazsa **Yıllık Net Üretim** ve **kapasite faktörü** “Hesaplanmadı” olur. Eksik dönem sıfır üretim kabul edilmez; kalan ölçümlerin genel ortalamasıyla yıllık üretim türetilmez.

Koşullar geçerse takvim aylarına göre ortalama net güç, normal 365 günlük yılın ay süreleriyle ağırlıklandırılır. Kapasite faktörü = yıllık net enerji / (kurulu güç × 8.760 saat). Bu sonuç bir ön tahmindir.

Bu kapsam eşikleri uygulama içi kontrollerdir; IEC/MEASNET standardı veya nihai AEP doğrulaması değildir. Uzun dönem temsil, yoğunluk, kalibrasyon ve akış modeli ayrıca doğrulanmalıdır. Menüdeki **P50/P75/P90**, mevcut sürümde kayıp paketi adlarıdır; istatistiksel aşılma olasılığı hesaplanmaz.
""")
    with st.expander("10 · Saha, harita, yerleşim ve çıktılarla çalışın"):
        st.markdown("""
KML/KMZ ile saha sınırını yükleyebilir, koordinatları ve çalışma alanını kontrol edebilir, türbin noktalarını oluşturabilir veya düzenleyebilirsiniz. Mevcut yerleşim ve mesafe kontrolleri hâkim rüzgâr yönü ile çapraz/rüzgâr altı açıklıkları değerlendirmeye yardımcı olur; nihai mühendislik uygunluk onayı değildir.

GWA rüzgâr haritası, topografya ve diğer harita araçları kaynak incelemesine yardımcı olur. Raster değerleri ve koordinat doğruluğu bağımsız doğrulanmadan enerji girdisi sayılmamalıdır. Yerleşim bazında yıllık AEP çıktısı mevcut sürümde kapalıdır; ortalama saha hızını doğrudan güç eğrisine uygulamak zaman serisi hesabının yerini tutmaz.

Aylık istatistikleri, kalite/kapsam raporunu, manuel işaretleri ve varsa tamamlama adaylarını ayrı CSV dosyaları olarak saklayın. Sonuçları paylaşırken direği, sensörü, dönemi, yükseklikleri, veri kapsamını, boşlukları, türbin eğrisini ve kayıp varsayımlarını belirtin.
""")
    st.warning("Açık doğrulamalar: Windows'ta gerçek kullanım ve görsel kontrol; farklı direk ve şemalarda kalite eşikleri; Windographer ile temiz veri eşdeğerliği; tamamlamanın bağımsız enerji doğrulaması; güç eğrisi/yoğunluk ve göbek dönüşümü; uzun dönem düzeltmesi, nihai AEP, gerçek P50/P75/P90 ve GWA raster doğruluğu. İnceleme kaydı veya kapsam kontrolü bu çalışmaların yerine geçmez.")
    st.stop()


if sayfa == "Ana Sayfa":
    st.markdown('## <span style="color: #000000;">Maki Wind Studio</span>', unsafe_allow_html=True)
    st.caption("Rüzgâr ölçümleri · Veri kalitesi · Micrositing")
    st.markdown("---")
    _h1, _h2, _h3 = st.columns(3)
    _h1.metric("Yüklü veri seti", len(dosyalar))
    _h2.metric("Santral sınırı", "Yüklü" if _v8_sinir_var else "Bekleniyor")
    _h3.metric("Sürüm", "v11.11.24")
    st.markdown("### " + ("Ölçümlerinizi kontrol ederek devam edin" if dosyalar else "İlk rüzgâr analizinize başlayın"))
    st.write("1. Veri yükleme  →  2. Rüzgâr Kaynağı Özeti  →  3. Enerji analizi")
    if dosyalar:
        st.info("Sıradaki adım: veri yükleme sayfasında ölçüm dosyalarınızı kontrol edin. Ardından Rüzgâr Kaynağı Özeti sayfasına geçerek aylık değerleri ve veri kalitesini inceleyin.")
        _home_label = "Devam et · Veri yükleme →"
    else:
        st.info("Sıradaki adım: LoggerNet rüzgâr ölçüm dosyanızı yükleyin. Uygulama sizi veri kontrolüne yönlendirecek.")
        _home_label = "Başla · Veri yükleme →"
    st.button(_home_label, type="primary", use_container_width=True,
              on_click=ana_sayfadan_veri_yuklemeye_git, key="home_continue_v111110")
    if dosyalar:
        st.caption(f"{len(dosyalar)} ölçüm dosyası yüklü. Dosya ve proje ayarlarına sol menüden ulaşabilirsiniz.")
    st.markdown("---")
    st.caption("Maki Enerji · RES Analiz ve Micrositing Platformu")
    st.stop()

# ============================================================
# RÜZGAR ÖLÇÜMLERİ: LOGGERNET OTOMATİK SENKRONİZASYON
# ============================================================
if sayfa == "Rüzgar Ölçümleri":
    arayuz_hero(
        "Rüzgar Ölçümleri",
        "LoggerNet'in her gün 11:00'de güncellediği WindData dosyaları otomatik algılanır ve analizlere aktarılır.",
        ["Otomatik senkronizasyon", "Kurulum raporu", "Direk tanıma", "Harici proje desteği"]
    )

    # Üç aşamalı, yönlendirmeli veri hazırlama akışı.
    if "ruzgar_olcumleri_adim_v112" not in st.session_state:
        st.session_state["ruzgar_olcumleri_adim_v112"] = int(app_state.get("measurement_step", 1) or 1)
    _olcum_adim = int(st.session_state["ruzgar_olcumleri_adim_v112"])
    app_state["measurement_step"] = _olcum_adim

    # Akış başlıkları artık tıklanabilir navigasyon butonlarıdır. Kullanıcı
    # herhangi bir aşamadan LoggerNet verilerine geri dönebilir; app_state
    # temizlenmediği için yüklenen dosyalar ve onaylanmış raporlar korunur.
    _adim_cols = st.columns(3)
    _adim_etiketleri = [(1, "1 · LoggerNet Verileri"), (2, "2 · Kurulum Raporları"), (3, "3 · Proje Özeti")]
    for _col, (_no, _etiket) in zip(_adim_cols, _adim_etiketleri):
        with _col:
            _aktif = _olcum_adim == _no
            if st.button(
                _etiket,
                key=f"ruzgar_olcumleri_adim_nav_{_no}_v1173",
                use_container_width=True,
                type="primary" if _aktif else "secondary",
            ):
                if _olcum_adim != _no:
                    st.session_state["ruzgar_olcumleri_adim_v112"] = _no
                    st.rerun()
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    if _olcum_adim == 2:
        _geri_col, _bos_col = st.columns([1.35, 4.65])
        with _geri_col:
            if st.button(
                "← LoggerNet Verilerine Dön",
                key="kurulumdan_loggernete_don_v1173",
                use_container_width=True,
            ):
                st.session_state["ruzgar_olcumleri_adim_v112"] = 1
                app_state["measurement_step"] = 1
                st.rerun()

        bolum_basligi(
            "Kurulum Raporundan Direk Ekle",
            "PDF kurulum/montaj raporunu yükleyin. Uygulama direk adı, koordinatlar, toplam yükseklik ve sensör seviyelerini önerir; kayıt yalnızca onayınızdan sonra kullanılır."
        )
        _mevcut_wind_adlari = [k.get("name", "") for k in app_state.get("wind_data_files", []) if k]
        if not _mevcut_wind_adlari:
            st.warning("Önce LoggerNet klasöründe en az bir WindData dosyası bulunmalı veya manuel veri yüklenmelidir.")
            st.stop()

        # Kullanıcı birden fazla direğin kurulum raporunu art arda ekleyebilir.
        # Bir rapor onaylandığında eksik raporlu sıradaki direğe geçilir; ancak
        # başka direk kalmadığında Proje Özeti aşaması otomatik açılır.
        _onayli_raporlar = app_state.get("mast_registry", {}) or {}
        _raporu_eksik_direkler = [
            ad for ad in _mevcut_wind_adlari if not _onayli_raporlar.get(ad)
        ]

        _durum_satirlari = [
            {
                "LoggerNet dosyası": ad,
                "Kurulum raporu": "Onaylandı" if _onayli_raporlar.get(ad) else "Bekliyor",
            }
            for ad in _mevcut_wind_adlari
        ]
        guvenli_dataframe(pd.DataFrame(_durum_satirlari), use_container_width=True, hide_index=True)

        _bekleyen_hedef = app_state.pop("pending_installation_report_target", None)
        if _bekleyen_hedef not in _mevcut_wind_adlari:
            _bekleyen_hedef = _raporu_eksik_direkler[0] if _raporu_eksik_direkler else _mevcut_wind_adlari[0]
        _hedef_index = _mevcut_wind_adlari.index(_bekleyen_hedef)

        _hedef_dosya = st.selectbox(
            "Raporun ait olduğu LoggerNet WindData dosyası",
            _mevcut_wind_adlari,
            index=_hedef_index,
            key="kurulum_raporu_hedef_dosya_v154",
        )

        _gecis_mesaji = st.session_state.pop("kurulum_raporu_gecis_mesaji_v154", None)
        if _gecis_mesaji:
            st.success(_gecis_mesaji)
        _rapor = st.file_uploader(
            "Direk kurulum raporu (PDF)",
            type=["pdf"],
            key=f"installation_report_uploader_{app_state.get('installation_report_nonce', 0)}",
            help="Metin katmanlı PDF'lerde otomatik okuma daha güçlüdür. Taranmış raporlarda bazı alanların elle doğrulanması gerekebilir.",
        )
        if _rapor is None:
            st.info("Kurulum raporunu yüklediğinizde tespit edilen bilgiler burada gösterilecek.")
            _kayit = app_state.get("mast_registry", {}).get(_hedef_dosya)
            if _kayit:
                _mast_adi = str(_kayit.get("mast_name") or "Direk")
                _kaynak_rapor = str(_kayit.get("source_report") or "Onaylı kurulum raporu")
                st.success(f"{_mast_adi} için kurulum raporu onaylı.")
                _ozet_parcalar = []
                if _kayit.get("mast_height_m"):
                    _ozet_parcalar.append(f"Direk yüksekliği: {_kayit.get('mast_height_m')} m")
                if _kayit.get("installation_date"):
                    _ozet_parcalar.append(f"Kurulum: {_kayit.get('installation_date')}")
                if _ozet_parcalar:
                    st.caption(" · ".join(_ozet_parcalar))

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button(
                "Kurulum raporu eklemeden devam et →",
                use_container_width=True,
                key="kurulum_raporu_eklemeden_devam_v126",
            ):
                st.session_state["ruzgar_olcumleri_adim_v112"] = 3
                app_state["measurement_step"] = 3
                st.rerun()
            st.stop()

        _rapor_sonuc = kurulum_raporu_pdf_oku(_rapor.getvalue())
        if _rapor_sonuc.get("hata"):
            st.error(f"Kurulum raporu okunamadı: {_rapor_sonuc['hata']}")
            st.stop()
        st.success("Kurulum raporu okundu.")

        # Müşteri ekranında yalnız konum ve sensör yükseklikleri gösterilir.
        # Diğer rapor alanları arka planda kayda alınmaya devam eder.
        _vars_ad = _rapor_sonuc.get("mast_name") or Path(_hedef_dosya).stem
        _mast_name = str(_vars_ad)
        _mast_h = float(_rapor_sonuc.get("mast_height_m") or 0.0)
        _coord_sys = str(_rapor_sonuc.get("coordinate_system") or "")
        _utm_east = float(_rapor_sonuc.get("utm_east") or 0.0)
        _utm_north = float(_rapor_sonuc.get("utm_north") or 0.0)
        _utm_zone = str(_rapor_sonuc.get("utm_zone") or "")
        _elevation = float(_rapor_sonuc.get("elevation_m") or 0.0)
        _install_date = str(_rapor_sonuc.get("installation_date") or "")

        st.markdown("#### Konum")
        _c1, _c2 = st.columns(2)
        with _c1:
            _lat = st.number_input(
                "Enlem",
                value=float(_rapor_sonuc.get("latitude") or 0.0),
                format="%.8f",
                key="report_lat_v1100",
            )
        with _c2:
            _lon = st.number_input(
                "Boylam",
                value=float(_rapor_sonuc.get("longitude") or 0.0),
                format="%.8f",
                key="report_lon_v1100",
            )

        st.markdown("#### Sensör yükseklikleri")
        _sens_cols = st.columns(3)
        _sensor_values = {}
        for _i, _kolon in enumerate(["WS1_Avg", "WS2_Avg", "WS3_Avg", "WS4_Avg", "WD1_Avg", "WD2_Avg"]):
            with _sens_cols[_i % 3]:
                _vars_y = float(_rapor_sonuc.get("sensors", {}).get(_kolon, 0.0))
                _sensor_values[_kolon] = st.number_input(
                    f"{_kolon} (m)",
                    min_value=0.0,
                    max_value=300.0,
                    value=_vars_y,
                    step=0.5,
                    key=f"report_sensor_{_kolon}_v1100",
                )

        _onay = st.checkbox("Bilgileri kontrol ettim; bu direk kaydına uygulanmasını onaylıyorum.", key="report_confirm_v94")
        if st.button("Direği Kaydet ve LoggerNet Verisiyle Eşleştir", type="primary", use_container_width=True, disabled=not _onay):
            if _lat == 0.0 or _lon == 0.0:
                st.error("Koordinatlar bulunamadı. Kaydetmeden önce enlem ve boylamı doğrulayın.")
            else:
                _kayit = {
                    "mast_name": _mast_name,
                    "source_report": _rapor.name,
                    "loggernet_file": _hedef_dosya,
                    "latitude": float(_lat), "longitude": float(_lon),
                    "coordinate_system": _coord_sys,
                    "utm_east": float(_utm_east) if _utm_east else None,
                    "utm_north": float(_utm_north) if _utm_north else None,
                    "utm_zone": _utm_zone,
                    "elevation_m": float(_elevation),
                    "mast_height_m": float(_mast_h),
                    "installation_date": _install_date,
                    "sensors": {k: float(v) for k, v in _sensor_values.items() if v > 0},
                    "approved_at": datetime.datetime.now().isoformat(timespec="seconds"),
                }
                rapor_kaydini_veri_setine_uygula(_hedef_dosya, _kayit)
                app_state.setdefault("mast_installation_reports", {})[_hedef_dosya] = dosyayi_kaydet(_rapor)
                # Yeni rapor için uploader ve form alanlarını temizle.
                app_state["installation_report_nonce"] = int(app_state.get("installation_report_nonce", 0)) + 1
                for _anahtar in list(st.session_state.keys()):
                    if (
                        _anahtar.startswith("report_")
                        or _anahtar == "kurulum_raporu_hedef_dosya_v154"
                    ):
                        del st.session_state[_anahtar]

                _kalan_direkler = [
                    ad for ad in _mevcut_wind_adlari
                    if not (app_state.get("mast_registry", {}) or {}).get(ad)
                ]
                kalici_durumu_kaydet(app_state)
                if _kalan_direkler:
                    _siradaki = _kalan_direkler[0]
                    app_state["pending_installation_report_target"] = _siradaki
                    st.session_state["kurulum_raporu_gecis_mesaji_v154"] = (
                        f"{_hedef_dosya} raporu onaylandı. Sıradaki direk: {_siradaki}"
                    )
                    st.session_state["ruzgar_olcumleri_adim_v112"] = 2
                    app_state["measurement_step"] = 2
                else:
                    st.session_state["ruzgar_olcumleri_adim_v112"] = 3
                    app_state["measurement_step"] = 3
                st.rerun()

        _kalan_sayi = len([
            ad for ad in _mevcut_wind_adlari
            if not (app_state.get("mast_registry", {}) or {}).get(ad)
        ])
        if _kalan_sayi:
            st.caption(
                f"{_kalan_sayi} direğin kurulum raporu henüz onaylanmadı. "
                "Raporları sırayla ekleyebilir veya dilediğiniz anda Proje Özeti'ne geçebilirsiniz."
            )
        else:
            st.success("Bütün direklerin kurulum raporları onaylandı.")

        if st.button(
            "Kurulum raporu girişini tamamla ve Proje Özeti'ne geç →",
            use_container_width=True,
            key="kurulum_raporlarini_tamamla_ozete_v154",
        ):
            st.session_state["ruzgar_olcumleri_adim_v112"] = 3
            app_state["measurement_step"] = 3
            st.rerun()
        st.stop()

    if _olcum_adim == 1:
        loggernet_klasoru = app_state.get("loggernet_folder", r"C:\Campbellsci\veriler")
        _bulut_klasor_baglantisi = os.name != "nt" and not Path(loggernet_klasoru).is_dir()
        st.caption("LoggerNet bağlantısı · v11.11.24")
        if _bulut_klasor_baglantisi or app_state.get("data_source") == "Tarayıcı LoggerNet klasörü":
            st.markdown("### Bilgisayarınızdaki LoggerNet klasörünü bağlayın")
            st.write("Sayfanın üstündeki LoggerNet otomatik bağlantı bölümünü açın. Klasörü bağla düğmesiyle C:\\Campbellsci\\veriler klasörünü seçip okuma izni verin. Dosyalar analiz için buluta aktarılır; asılları değiştirilmez.")
        manuel_mod = app_state.get("data_source") == "Manuel dosya yükleme"
        if manuel_mod:
            st.warning("Şu anda harici proje için manuel veri seti kullanılıyor.")
            if st.button("LoggerNet otomatik verilerine dön", type="primary"):
                app_state["data_source"] = "LoggerNet klasörü"
                app_state["wind_data_files"] = []
                st.rerun()
        if app_state.get("data_source") == "Tarayıcı LoggerNet klasörü":
            st.markdown("### 📡 LoggerNet · Tarayıcıdan otomatik aktarım")
            st.info("Bağladığınız klasör açık sekmede 15 saniyede bir kontrol edilir. Dosyalar salt okunur; LoggerNet dosyası değiştirilmez. Son tarama ve canlı takip durumu yukarıdaki bağlantı panelindedir. Tarayıcı uykuya geçerse takip gecikebilir veya durabilir.")
            _browser_records = app_state.get("wind_data_files", [])
            st.metric("Son alınan dosya sayısı", len(_browser_records))
            st.caption("Aşağıdaki liste son başarıyla alınan dosyaları gösterir; klasöre erişimin şu anda sürdüğünü tek başına kanıtlamaz. Bağlantı kesilirse son veri korunur, yeni veri alınmış sayılmaz.")
            guvenli_dataframe(pd.DataFrame([{"Dosya": x["name"], "Boyut (MB)": round(x["size"] / 1024**2, 2), "Kaynak dosya güncellemesi": datetime.datetime.fromtimestamp(x["mtime_ms"] / 1000).strftime("%d.%m.%Y %H:%M:%S")} for x in _browser_records]), use_container_width=True, hide_index=True)
        elif _bulut_klasor_baglantisi:
            st.info("Klasör izni bekleniyor. Üstteki Klasörü bağla düğmesini kullanın. İzin verilmeden bilgisayarınızdaki klasör bulutta okunamaz.")
            st.caption("Desteklenmiyor veya izin hatası görürseniz bu uygulama adresini güncel Chrome/Edge içinde açın. Otomatik takip için sekme açık ve bilgisayar internete bağlı kalmalıdır.")
        else:
            bulunan_loggernet = loggernet_winddata_dosyalarini_bul(loggernet_klasoru)

            st.markdown("### 📡 LoggerNet Veri Senkronizasyonu")
            st.caption("LoggerNet veri toplama işlemini yapar; Maki Wind Studio yalnızca güncellenen **WindData.dat** dosyalarını otomatik okur. **RawData.dat** dosyaları kullanılmaz.")

            son_veri_iso = app_state.get("loggernet_last_data_update")
            son_tarama_iso = app_state.get("loggernet_last_scan")
            son_veri = datetime.datetime.fromisoformat(son_veri_iso) if son_veri_iso else None
            son_tarama = datetime.datetime.fromisoformat(son_tarama_iso) if son_tarama_iso else None
            simdi = datetime.datetime.now()
            veri_yasi_saat = ((simdi - son_veri).total_seconds() / 3600.0) if son_veri else None

            if not Path(loggernet_klasoru).is_dir():
                durum_metni = "Klasör bulunamadı"
            elif not bulunan_loggernet:
                durum_metni = "WindData bekleniyor"
            elif veri_yasi_saat is not None and veri_yasi_saat > 48:
                durum_metni = "Kontrol gerekli"
            else:
                durum_metni = "Güncel"

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Bağlantı durumu", "Bağlı" if bulunan_loggernet else "Bağlantı yok")
            k2.metric("Bulunan direk", len(bulunan_loggernet))
            k3.metric("Son dosya güncellemesi", son_veri.strftime("%d.%m.%Y %H:%M") if son_veri else "—")
            k4.metric("Veri durumu", durum_metni)

            yol_col, yenile_col = st.columns([5, 1])
            with yol_col:
                yeni_klasor = st.text_input(
                    "LoggerNet veri klasörü",
                    value=loggernet_klasoru,
                    key="loggernet_klasor_widget_v83",
                    help=r"Varsayılan klasör: C:\Campbellsci\veriler",
                )
            with yenile_col:
                st.write("")
                st.write("")
                elle_yenile = st.button("🔄 Şimdi kontrol et", type="primary", use_container_width=True)

            if yeni_klasor != loggernet_klasoru:
                app_state["loggernet_folder"] = yeni_klasor
                app_state["loggernet_last_scan"] = None
                st.rerun()
            if elle_yenile:
                st.rerun()

            yeni_dosyalar = app_state.get("loggernet_new_files", [])
            degisen_dosyalar = app_state.get("loggernet_changed_files", [])
            if yeni_dosyalar:
                st.success("Yeni direk algılandı: " + ", ".join(yeni_dosyalar))
                app_state["loggernet_new_files"] = []
            elif degisen_dosyalar:
                st.success("Yeni LoggerNet verisi algılandı ve analiz seti güncellendi: " + ", ".join(degisen_dosyalar))
                app_state["loggernet_changed_files"] = []

            if bulunan_loggernet:
                tablo = []
                for kayit in bulunan_loggernet:
                    dt = datetime.datetime.fromtimestamp(Path(kayit["source_path"]).stat().st_mtime)
                    yas_saat = max((simdi - dt).total_seconds() / 3600.0, 0.0)
                    tablo.append({
                        "Direk / dosya": kayit["name"],
                        "Boyut (MB)": round(kayit["size"] / (1024 * 1024), 1),
                        "Son güncelleme": dt.strftime("%d.%m.%Y %H:%M:%S"),
                        "Durum": "Güncel" if yas_saat <= 48 else "Kontrol gerekli",
                    })
                guvenli_dataframe(pd.DataFrame(tablo), use_container_width=True, hide_index=True)
                tarama_metni = son_tarama.strftime("%d.%m.%Y %H:%M:%S") if son_tarama else "—"
                st.info(f"Son klasör kontrolü: **{tarama_metni}** · LoggerNet her gün 11:00'de dosyaları güncellediğinde uygulama bir sonraki ekran yenilemesinde değişikliği otomatik algılar.")
            elif Path(loggernet_klasoru).is_dir():
                st.warning("Klasör bulundu ancak `WindData.dat` ile biten dosya bulunamadı.")
            else:
                if os.name != "nt":
                    st.info("Bulut uygulaması Windows klasörünü doğrudan göremez. Sayfanın üstündeki LoggerNet otomatik bağlantı bölümünde Klasörü bağla düğmesine basın ve C:\\Campbellsci\\veriler klasörünü seçin. Sonraki güncellemeler sekme açıkken otomatik alınır.")
                else:
                    st.error(f"LoggerNet klasörü bulunamadı: {loggernet_klasoru}")

        with st.expander("Farklı bir proje için manuel dosya yükle", expanded=False):
            st.caption("Otomatik klasör bağlantısından bağımsız bir veri seti yükler. Mevcut çalışma setini değiştirir; otomatik klasör takibi duraklatılır.")
            yuklenen_wind_dosyalari = st.file_uploader(
                "Manuel wind data dosyalarını seçin",
                type=["dat", "csv"],
                accept_multiple_files=True,
                key=f"wind_data_uploader_{app_state['wind_uploader_nonce']}",
            )
            if yuklenen_wind_dosyalari and yukleme_listesi_degisti(
                yuklenen_wind_dosyalari, app_state.get("wind_data_files", [])
            ):
                app_state["wind_data_files"] = [dosyayi_kaydet(d) for d in yuklenen_wind_dosyalari]
                app_state["data_source"] = "Manuel dosya yükleme"
                st.success(f"{len(yuklenen_wind_dosyalari)} manuel dosya çalışma setine alındı.")
                st.rerun()

        dosyalar = [
            kayitli_dosyayi_olustur(kayit)
            for kayit in app_state.get("wind_data_files", [])
            if kayit
        ]

        if not dosyalar:
            st.markdown(
                '<div class="empty-state"><h3>WindData bulunamadı</h3><p>Yerel çalışmada klasör yolunu kontrol edin. Bulutta sayfanın üstündeki LoggerNet otomatik bağlantı bölümünden klasöre okuma izni verin.</p></div>',
                unsafe_allow_html=True,
            )
            st.stop()

        st.success(f"{len(dosyalar)} rüzgâr veri dosyası hazır. Rüzgâr Kaynağı Özeti'ne geçerek analize devam edebilirsiniz.")
        st.caption("Direk bilgilerini düzenlemek için üstteki Kurulum Raporları bölümünü kullanabilirsiniz.")
        st.button("Devam et · Rüzgâr Kaynağı Özeti →", type="primary", use_container_width=True,
                  key="yuklemeden_ruzgar_ozetine_v111111", on_click=navigasyona_git,
                  args=("Rüzgar Kaynağı Özeti",))
        st.stop()
if sayfa != "Rüzgar Ölçümleri" or (sayfa == "Rüzgar Ölçümleri" and int(st.session_state.get("ruzgar_olcumleri_adim_v112", 1)) == 3):
    dosyalar = [
        kayitli_dosyayi_olustur(kayit)
        for kayit in app_state.get("wind_data_files", [])
        if kayit
    ]

# Diğer analiz sayfalarında dosya yoksa hata yerine yönlendirici ekran göster.
if not dosyalar:
    arayuz_hero(
        "Önce Rüzgar Ölçümlerini Yükleyin",
        "Bu modülün çalışabilmesi için en az bir LoggerNet .dat veya .csv dosyası gereklidir.",
        ["Veri gerekli", "Rüzgar Ölçümleri", "Oturum korumalı"]
    )
    st.info("Sol menüden **Rüzgar Ölçümleri** sayfasına geçerek wind data yükleyin.")
    st.button(
        "Rüzgar Ölçümleri sayfasına git",
        type="primary",
        on_click=navigasyona_git,
        args=("Rüzgar Ölçümleri",),
    )
    st.stop()

# Her yükleme ayrı bir veri setidir. Aynı dosya adı iki kez yüklense bile
# birbirinin üzerine yazmaması için benzersiz veri seti anahtarı kullanılır.
tum_veri_setleri = {}
tum_dosya_kalite_ozeti = []
veri_seti_orijinal_adlari = {}
veri_seti_kaynak_dosyalari = {}
with st.spinner("Wind data dosyaları okunuyor..."):
    for dosya_sirasi, yuklenen_dosya in enumerate(dosyalar, start=1):
        try:
            if getattr(yuklenen_dosya, "source_path", None):
                _stat = Path(yuklenen_dosya.source_path).stat()
                veri_seti = loggernet_oku_yoldan(
                    yuklenen_dosya.source_path, int(_stat.st_mtime_ns), int(_stat.st_size)
                )
            else:
                veri_seti = loggernet_oku(yuklenen_dosya.getvalue())
            if not veri_seti.empty:
                veri_seti_anahtari = f"Direk {dosya_sirasi} · {yuklenen_dosya.name}"
                tum_veri_setleri[veri_seti_anahtari] = veri_seti
                _all_mask, _all_reason, _all_events, _all_time = otomatik_olcum_kontrolu(veri_seti)
                tum_dosya_kalite_ozeti.append({
                    "Veri seti":veri_seti_anahtari,"Kayıt":len(veri_seti),
                    "Hız sensörü":len(hiz_sensor_kolonlari(veri_seti)),
                    "Kayıt aralığı (dk)":_all_time["step_seconds"]/60,
                    "Otomatik kalite olayı":len(_all_events),
                    "Zaman ekseni":"Uygun" if _all_time["cadence_ok"] and not _all_time["duplicates"] and not _all_time["invalid_times"] else "İnceleme gerekli",
                    "Çapraz sensör kontrolü":"Var" if len(hiz_sensor_kolonlari(veri_seti))>=3 else "Yetersiz sensör"})
                veri_seti_orijinal_adlari[veri_seti_anahtari] = yuklenen_dosya.name
                veri_seti_kaynak_dosyalari[veri_seti_anahtari] = yuklenen_dosya
        except Exception as hata:
            st.sidebar.error(f"{yuklenen_dosya.name} okunamadı: {hata}")

if not tum_veri_setleri:
    st.error("Yüklenen dosyalardan geçerli bir wind data okunamadı.")
    st.stop()

_veri_seti_adlari = list(tum_veri_setleri.keys())

def veri_seti_gorunur_adi(veri_seti_anahtari):
    """WindData anahtarını, varsa kurulum raporundaki direk adıyla gösterir."""
    orijinal = veri_seti_orijinal_adlari.get(veri_seti_anahtari, veri_seti_anahtari)
    kayit = (app_state.get("mast_registry", {}).get(orijinal)
             or app_state.get("mast_registry", {}).get(veri_seti_anahtari))
    mast_name = str((kayit or {}).get("mast_name") or "").strip()
    return f"{mast_name} · {orijinal}" if mast_name else veri_seti_anahtari


def _mast_esleme_norm(x):
    """Dosya/direk adlarını Türkçe karakter, uzantı ve genel eklerden arındırır."""
    x = str(x or "").lower().replace("ı", "i").replace("ş", "s").replace("ğ", "g")
    x = x.replace("ü", "u").replace("ö", "o").replace("ç", "c")
    x = re.sub(r"\.(dat|csv|txt)$", "", x)
    x = re.sub(r"(?:maki|winddata|rawdata|loggernet|direk|mast)", "", x)
    return re.sub(r"[^a-z0-9]+", "", x)


def veri_seti_mast_kaydi(veri_seti_anahtari):
    """Veri setine bağlı kurulum raporu kaydını güvenli biçimde bulur.

    Eski sürümlerde kayıt anahtarı bazen orijinal dosya adı, bazen ``Direk N ·``
    etiketi olarak saklandı. Bu işlev her iki yapıyı ve kaydın loggernet_file /
    mast_name alanlarını birlikte değerlendirir.
    """
    kayitlar = app_state.get("mast_registry", {}) or {}
    orijinal = veri_seti_orijinal_adlari.get(veri_seti_anahtari, veri_seti_anahtari)
    dogrudan = kayitlar.get(orijinal) or kayitlar.get(veri_seti_anahtari)
    if dogrudan:
        return dogrudan

    adaylar = {
        _mast_esleme_norm(veri_seti_anahtari),
        _mast_esleme_norm(orijinal),
    }
    adaylar.discard("")
    for anahtar, kayit in kayitlar.items():
        kayit = kayit or {}
        hedefler = {
            _mast_esleme_norm(anahtar),
            _mast_esleme_norm(kayit.get("mast_name")),
            _mast_esleme_norm(kayit.get("loggernet_file")),
        }
        hedefler.discard("")
        if any(a == h or a in h or h in a for a in adaylar for h in hedefler):
            return kayit

    # Tek veri seti + tek onaylı direk kaydı varsa bunun aynı direk olduğu açıktır.
    if len(_veri_seti_adlari) == 1 and len(kayitlar) == 1:
        return next(iter(kayitlar.values()))
    return None


def onceki_sensor_yuksekliklerini_bul(veri_seti_anahtari):
    """Eski sürümlerde farklı anahtarla saklanan pozitif sensör seviyelerini bulur."""
    tumu = app_state.get("sensor_heights", {}) or {}
    orijinal = veri_seti_orijinal_adlari.get(veri_seti_anahtari, veri_seti_anahtari)
    adaylar = {_mast_esleme_norm(veri_seti_anahtari), _mast_esleme_norm(orijinal)}
    adaylar.discard("")
    for eski_anahtar, yukler in tumu.items():
        hedef = _mast_esleme_norm(eski_anahtar)
        if hedef and any(a == hedef or a in hedef or hedef in a for a in adaylar):
            bulunan = {
                k: float(v) for k, v in (yukler or {}).items()
                if k in RUZGAR_KOLONLARI and v is not None and float(v) > 0
            }
            if bulunan:
                return bulunan
    return {}
# Tüm yüklenmiş WindData dosyaları çalışma setinde her zaman seçilebilir.
# Kurulum raporu eşleşmesi yalnızca görünen direk adını ve sensör/konum bilgisini
# zenginleştirir; bir veri setini seçim listesinden düşürmez.
_raporlu_veri_setleri = [
    ad for ad in _veri_seti_adlari
    if veri_seti_mast_kaydi(ad) is not None
]
_secilebilir_veri_setleri = list(_veri_seti_adlari)

_kayitli_secimler = [
    ad for ad in app_state.get("selected_wind_data", [])
    if ad in _secilebilir_veri_setleri
]

# Aynı oturumda yüklenen WindData sayısı ile onaylı direk raporu sayısı eşitse,
# eski sürümden tek-direk olarak kalmış seçimleri otomatik olarak bütün direklere genişlet.
_onayli_rapor_sayisi = len(app_state.get("mast_registry", {}) or {})
if (
    len(_secilebilir_veri_setleri) >= 2
    and _onayli_rapor_sayisi == len(_secilebilir_veri_setleri)
    and len(_kayitli_secimler) < len(_secilebilir_veri_setleri)
):
    _kayitli_secimler = list(_secilebilir_veri_setleri)

if not _kayitli_secimler:
    if _raporlu_veri_setleri:
        _kayitli_secimler = list(_raporlu_veri_setleri)
    else:
        _onceki_aktif = app_state.get("active_wind_data")
        _kayitli_secimler = [
            _onceki_aktif
            if _onceki_aktif in _secilebilir_veri_setleri
            else _secilebilir_veri_setleri[0]
        ]

# Bir veri seti seçimi bütün özet ve veri inceleme bileşenlerine aktarılır.
_tek_aktif = app_state.get("active_wind_data")
if _tek_aktif not in _secilebilir_veri_setleri:
    _tek_aktif = _kayitli_secimler[0]
if sayfa in {"Rüzgar Kaynağı Özeti", "Veri İnceleme"}:
    st.markdown("### " + ("Rüzgâr Kaynağı Özeti" if sayfa == "Rüzgar Kaynağı Özeti" else "Veri İnceleme"))
    _selection_key = "tek_veri_secimi_v11119"
    if st.session_state.get(_selection_key) not in _secilebilir_veri_setleri:
        st.session_state[_selection_key] = _tek_aktif
    _tek_aktif = st.selectbox("Veri seti", options=_secilebilir_veri_setleri,
                             format_func=veri_seti_gorunur_adi, key=_selection_key)
secili_veri_setleri = [_tek_aktif]
app_state["selected_wind_data"] = list(secili_veri_setleri)
aktif_dosya_adi = _tek_aktif
app_state["active_wind_data"] = aktif_dosya_adi

# Her wind data / ölçüm direği kendi sensör yüksekliği ayarlarını taşır.
# Ayarlar dosya adı bazında saklanır ve o veri setinin bütün grafik ve hesaplarında kullanılır.
app_state.setdefault("sensor_heights", {})
for _dosya_adi in _veri_seti_adlari:
    _algilanan = loggernet_sensor_yuksekliklerini_algila(
        veri_seti_kaynak_dosyalari.get(_dosya_adi)
    ) if _dosya_adi in veri_seti_kaynak_dosyalari else {}
    _orijinal_ad = veri_seti_orijinal_adlari.get(_dosya_adi, _dosya_adi)
    _rapor_kaydi = veri_seti_mast_kaydi(_dosya_adi)
    # Önce eski sürümde başka veri-seti anahtarı altında kalmış yükseklikleri taşı.
    _algilanan.update(onceki_sensor_yuksekliklerini_bul(_dosya_adi))
    if _rapor_kaydi:
        # Kurulum raporundaki onaylanmış sensör seviyeleri analiz anahtarına
        # mutlaka taşınır. Kayıt dosya adıyla tutulsa bile grafikler
        # ``Direk N · dosya`` anahtarını kullandığı için burada eşitlenir.
        _rapor_sensorleri = {
            k: float(v)
            for k, v in (_rapor_kaydi.get("sensors", {}) or {}).items()
            if k in RUZGAR_KOLONLARI and v is not None and float(v) > 0
        }
        _algilanan.update(_rapor_sensorleri)
    if _dosya_adi not in app_state["sensor_heights"]:
        _ilk_yukseklikler = {k: 0.0 for k in RUZGAR_KOLONLARI}
        _ilk_yukseklikler.update(_algilanan)
        app_state["sensor_heights"][_dosya_adi] = _ilk_yukseklikler
    elif _algilanan:
        # Kurulum raporu bağlıysa rapordaki doğrulanmış yükseklikler eski oturum
        # değerlerinin üzerine yazılır. Yalnız LoggerNet algısı varsa boş alanları doldurur.
        for _kolon, _deger in _algilanan.items():
            if _kolon not in RUZGAR_KOLONLARI:
                continue
            _deger = float(_deger or 0.0)
            _mevcut = app_state["sensor_heights"][_dosya_adi].get(_kolon)
            if _rapor_kaydi or _mevcut in (None, 0.0):
                app_state["sensor_heights"][_dosya_adi][_kolon] = _deger
                st.session_state[f"sensor_height::{_dosya_adi}::{_kolon}"] = _deger
                # Eski sürümlerde dosya adıyla oluşturulmuş widget anahtarını da
                # güncel tut; böylece yeniden çalıştırmada 0 değeri geri basılmaz.
                st.session_state[f"sensor_height::{_orijinal_ad}::{_kolon}"] = _deger

if sayfa == "Rüzgar Ölçümleri" and int(st.session_state.get("ruzgar_olcumleri_adim_v112", 1)) != 3:
    st.markdown("### Her wind data için ayrı sensör yükseklikleri")
    st.caption(
        "Her wind data için sensör kolonlarını ve ölçüm yüksekliklerini ayrı ayrı girin. "
        "Kaydedilen değerler yalnızca ilgili veri setinin grafik, shear, temizleme, hub yüksekliği ve üretim hesaplarında kullanılır."
    )

    for _sira, _dosya_adi in enumerate(_veri_seti_adlari, start=1):
        _dosya_yukseklikleri = app_state["sensor_heights"][_dosya_adi]
        with st.expander(
            f"{_sira}. direk · {_dosya_adi}",
            expanded=(_dosya_adi == aktif_dosya_adi)
        ):
            _yuk_cols = st.columns(4)
            for _idx, _kolon in enumerate(RUZGAR_KOLONLARI):
                with _yuk_cols[_idx]:
                    _widget_key = f"sensor_height::{_dosya_adi}::{_kolon}"
                    if _widget_key not in st.session_state:
                        st.session_state[_widget_key] = float(
                            _dosya_yukseklikleri.get(
                                _kolon,
                                0.0
                            )
                        )
                    _yeni_yukseklik = st.number_input(
                        f"{_kolon} yüksekliği (m)",
                        min_value=0.0,
                        max_value=300.0,
                        step=0.5,
                        key=_widget_key,
                    )
                    _dosya_yukseklikleri[_kolon] = float(_yeni_yukseklik)

            _otomatik_yuk = loggernet_sensor_yuksekliklerini_algila(
                veri_seti_kaynak_dosyalari.get(_dosya_adi)
            ) if _dosya_adi in veri_seti_kaynak_dosyalari else {}
            if _otomatik_yuk:
                st.success(
                    "LoggerNet başlığından otomatik algılandı: "
                    + ", ".join(f"{k}={v:g} m" for k, v in _otomatik_yuk.items())
                )
            else:
                st.info(
                    "Bu LoggerNet dosyasında sensör yüksekliği açıkça yazmıyor. "
                    "Kaydedilmiş direk ayarı kullanılıyor; bir kez doğrulamanız yeterli."
                )

aktif_yukseklikler = app_state["sensor_heights"][aktif_dosya_adi]
AKTIF_SENSOR_YUKSEKLIKLERI = sensor_yukseklik_tuple(aktif_yukseklikler)
AKTIF_GORUNUR_ADLAR = {
    k: sensor_etiketi(k, aktif_yukseklikler)
    for k in RUZGAR_KOLONLARI
}

# Direk koordinatları Ana Sayfa üst bölümünden yönetilir.
# Bilinen örnek direk adları için başlangıç koordinatları otomatik doldurulabilir.
VARSAYILAN_DIREK_KOORDINATLARI = {
    "corlu-1": {"lat": 41.138150, "lon": 27.693830},
    "çorlu-1": {"lat": 41.138150, "lon": 27.693830},
    "corlu-2": {"lat": 41.119680, "lon": 27.665502},
    "çorlu-2": {"lat": 41.119680, "lon": 27.665502},
}

def varsayilan_direk_konumu(dosya_adi):
    # Benzersiz etiket içinde orijinal dosya adı da bulunduğu için eşleştirme çalışır.
    ad = dosya_adi.lower()
    for anahtar, koordinat in VARSAYILAN_DIREK_KOORDINATLARI.items():
        if anahtar in ad:
            return koordinat
    return None

# Widget değerlerini sayfalar arasında korumak için session_state hazırlanır.
# Kurulum raporunda koordinat varsa her iki koordinat ekranına da otomatik uygulanır.
# Eski sürümde number_input, value verilmediği için -90 / -180 sınırlarına düşebiliyordu;
# bu geçersiz kalıntılar da rapor koordinatlarıyla otomatik düzeltilir.
def _gecerli_direk_koordinati(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        return (-90.0 < lat < 90.0) and (-180.0 < lon < 180.0) and not (lat == 0.0 and lon == 0.0)
    except Exception:
        return False

for sira, dosya_adi in enumerate(tum_veri_setleri.keys(), start=1):
    _rapor_konum = veri_seti_mast_kaydi(dosya_adi) or {}
    _rapor_lat = float(_rapor_konum.get("latitude") or 0.0)
    _rapor_lon = float(_rapor_konum.get("longitude") or 0.0)
    _rapor_gecerli = _gecerli_direk_koordinati(_rapor_lat, _rapor_lon)
    _isim_varsayilani = varsayilan_direk_konumu(dosya_adi)
    varsayilan = ({"lat": _rapor_lat, "lon": _rapor_lon} if _rapor_gecerli else _isim_varsayilani)

    kullan_key = f"direk_kullan_{sira}"
    lat_key = f"direk_lat_{sira}"
    lon_key = f"direk_lon_{sira}"

    _mevcut_lat = st.session_state.get(lat_key)
    _mevcut_lon = st.session_state.get(lon_key)
    _mevcut_gecerli = _gecerli_direk_koordinati(_mevcut_lat, _mevcut_lon)

    # Rapor kaydı en güvenilir kaynaktır. Boş, sınır değeri veya önceki hatalı değerleri düzelt.
    if _rapor_gecerli and (not _mevcut_gecerli or _mevcut_lat in (-90.0, 90.0) or _mevcut_lon in (-180.0, 180.0)):
        st.session_state[lat_key] = _rapor_lat
        st.session_state[lon_key] = _rapor_lon
        st.session_state[kullan_key] = True
    else:
        if kullan_key not in st.session_state:
            st.session_state[kullan_key] = varsayilan is not None
        if lat_key not in st.session_state:
            st.session_state[lat_key] = varsayilan["lat"] if varsayilan else 0.0
        if lon_key not in st.session_state:
            st.session_state[lon_key] = varsayilan["lon"] if varsayilan else 0.0

# Koordinatları session_state üzerinden oluştur; böylece Üretim Hesaplama
# sayfası da Ana Sayfa'da girilen değerleri kullanabilir.
direk_koordinatlari = {}
for sira, dosya_adi in enumerate(tum_veri_setleri.keys(), start=1):
    konum_kullan = bool(st.session_state.get(f"direk_kullan_{sira}", False))
    lat = float(st.session_state.get(f"direk_lat_{sira}", 0.0))
    lon = float(st.session_state.get(f"direk_lon_{sira}", 0.0))
    if konum_kullan and not (lat == 0.0 and lon == 0.0):
        direk_koordinatlari[dosya_adi] = {"lat": lat, "lon": lon}

ham_veri = tum_veri_setleri[aktif_dosya_adi]
secili_tum_veriler = {ad: tum_veri_setleri[ad] for ad in secili_veri_setleri}

# ============================================================
# SEÇİLİ DOSYALARIN TARİH ARALIĞI
# ============================================================

dosya_min_tarih = min(
    veri["TIMESTAMP"].min().date() for veri in secili_tum_veriler.values()
)
dosya_max_tarih = max(
    veri["TIMESTAMP"].max().date() for veri in secili_tum_veriler.values()
)

varsayilan_baslangic = app_state.get("date_start") or dosya_min_tarih
varsayilan_bitis = app_state.get("date_end") or dosya_max_tarih
varsayilan_baslangic = max(dosya_min_tarih, min(varsayilan_baslangic, dosya_max_tarih))
varsayilan_bitis = max(dosya_min_tarih, min(varsayilan_bitis, dosya_max_tarih))

# Tarih seçimi de çalışma setiyle birlikte özet sayfasına taşındı.
if sayfa in {"Rüzgar Kaynağı Özeti", "Veri İnceleme"}:
    tarih_sol, tarih_sag = st.columns(2)
    with tarih_sol:
        baslangic_tarihi = st.date_input(
            "Analiz başlangıcı", value=varsayilan_baslangic,
            min_value=dosya_min_tarih, max_value=dosya_max_tarih,
            key=f"ozet_baslangic_tarihi_{aktif_dosya_adi}"
        )
    with tarih_sag:
        bitis_tarihi = st.date_input(
            "Analiz bitişi", value=varsayilan_bitis,
            min_value=dosya_min_tarih, max_value=dosya_max_tarih,
            key=f"ozet_bitis_tarihi_{aktif_dosya_adi}"
        )
else:
    baslangic_tarihi = varsayilan_baslangic
    bitis_tarihi = varsayilan_bitis

app_state["date_start"] = baslangic_tarihi
app_state["date_end"] = bitis_tarihi

if baslangic_tarihi > bitis_tarihi:
    st.error(
        "Başlangıç tarihi bitiş tarihinden "
        "sonra olamaz."
    )
    st.stop()


filtreli_veri = ham_veri[
    (ham_veri["TIMESTAMP"].dt.date >= baslangic_tarihi)
    & (ham_veri["TIMESTAMP"].dt.date <= bitis_tarihi)
].copy()

secili_filtreli_veriler = {}
for _ad, _veri in secili_tum_veriler.items():
    _filtreli = _veri[
        (_veri["TIMESTAMP"].dt.date >= baslangic_tarihi)
        & (_veri["TIMESTAMP"].dt.date <= bitis_tarihi)
    ].copy()
    if not _filtreli.empty:
        secili_filtreli_veriler[_ad] = _filtreli

if filtreli_veri.empty:
    st.warning(
        "Seçilen tarih aralığında veri bulunamadı."
    )
    st.stop()


# ============================================================
# ORTAK BAŞLIK
# ============================================================

# Rüzgar Ölçümleri içindeki adımlarda kendi başlığı kullanılır; proje özeti
# ekranında ikinci ve tekrarlı kahraman başlığı gösterilmez.
if sayfa not in {"Rüzgar Ölçümleri", "Rüzgar Kaynağı Özeti", "Veri İnceleme"}:
    arayuz_hero(
        "RES Analiz ve Micrositing Platformu",
        "Ölçüm verisinden rüzgar kaynağı değerlendirmesine, türbin yerleşiminden yıllık net üretime kadar tüm ön analiz adımları.",
        [
            f"{baslangic_tarihi.strftime('%d.%m.%Y')} – {bitis_tarihi.strftime('%d.%m.%Y')}",
            f"{len(filtreli_veri):,} kayıt",
            f"Seçili veri · {len(secili_veri_setleri)} direk",
            "2,5D × 6D gerçek elips"
        ]
    )

    st.markdown(
        f"""
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin:-2px 0 18px;color:#5f7169;font-size:.78rem;">
            <span style="background:white;border:1px solid #dfe7e2;border-radius:999px;padding:7px 10px;">● Sistem hazır</span>
            <span style="background:white;border:1px solid #dfe7e2;border-radius:999px;padding:7px 10px;">{len(tum_veri_setleri)} veri seti</span>
            <span style="background:white;border:1px solid #dfe7e2;border-radius:999px;padding:7px 10px;">{len(direk_koordinatlari)} konumlu direk</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# RÜZGAR ÖLÇÜMLERİ ÖZETİ
# ============================================================

if sayfa == "Rüzgar Ölçümleri":
    _rapor_kayitlari = app_state.get("mast_registry", {})

    if not _rapor_kayitlari:
        bolum_basligi(
            "Direk Özeti",
            "Henüz onaylanmış bir kurulum raporu bulunmuyor. Önce istediğiniz direğin kurulum raporunu yükleyin."
        )
        if st.button("← Kurulum raporuna dön", use_container_width=True, key="ozetten_rapora_bos_v124"):
            st.session_state["ruzgar_olcumleri_adim_v112"] = 2
            app_state["measurement_step"] = 2
            st.rerun()
        st.stop()

    _raporlu_dosyalar = list(_rapor_kayitlari.keys())
    _son_hedef = st.session_state.get("kurulum_raporu_hedef_dosya_v93")
    _varsayilan_indeks = _raporlu_dosyalar.index(_son_hedef) if _son_hedef in _raporlu_dosyalar else 0

    if len(_raporlu_dosyalar) > 1:
        _ozet_dosya = st.selectbox(
            "Özeti gösterilecek direk",
            _raporlu_dosyalar,
            index=_varsayilan_indeks,
            format_func=lambda ad: _rapor_kayitlari.get(ad, {}).get("mast_name") or ad,
            key="direk_ozeti_secimi_v124",
        )
    else:
        _ozet_dosya = _raporlu_dosyalar[0]

    _mast = _rapor_kayitlari[_ozet_dosya]
    _veri_seti = tum_veri_setleri.get(_ozet_dosya)
    if _veri_seti is None:
        _rapor_loggernet = Path(str(_mast.get("loggernet_file") or _ozet_dosya)).name.lower()
        for _vs_anahtar, _orijinal_ad in veri_seti_orijinal_adlari.items():
            if (
                Path(str(_orijinal_ad)).name.lower() == Path(str(_ozet_dosya)).name.lower()
                or Path(str(_orijinal_ad)).name.lower() == _rapor_loggernet
            ):
                _veri_seti = tum_veri_setleri.get(_vs_anahtar)
                break
    _sensorler = _mast.get("sensors", {}) or {}

    bolum_basligi(
        f"{_mast.get('mast_name') or Path(_ozet_dosya).stem} · Direk Özeti",
        "Onaylanan kurulum raporundan alınan direk, koordinat ve sensör bilgileri."
    )

    _k1, _k2, _k3, _k4 = st.columns(4)
    _k1.metric("LoggerNet dosyası", Path(_ozet_dosya).name)
    _k2.metric("Kayıt sayısı", f"{len(_veri_seti):,}" if _veri_seti is not None else "—")
    _k3.metric("Direk tepe yüksekliği", f"{float(_mast.get('mast_height_m') or 0):g} m" if _mast.get("mast_height_m") else "—")
    _k4.metric("Rakım", f"{float(_mast.get('elevation_m') or 0):g} m" if _mast.get("elevation_m") is not None else "—")

    _sol, _sag = st.columns(2)
    with _sol:
        st.markdown("#### Genel bilgiler")
        _genel = pd.DataFrame([
            {"Alan": "Direk adı", "Değer": _mast.get("mast_name") or "—"},
            {"Alan": "Kurulum tarihi", "Değer": _mast.get("installation_date") or "—"},
            {"Alan": "Kurulum raporu", "Değer": _mast.get("source_report") or "—"},
            {"Alan": "Koordinat sistemi", "Değer": _mast.get("coordinate_system") or "—"},
            {"Alan": "Onay zamanı", "Değer": _mast.get("approved_at") or "—"},
        ])
        guvenli_dataframe(_genel, use_container_width=True, hide_index=True)

    with _sag:
        st.markdown("#### Konum bilgileri")
        _konum = pd.DataFrame([
            {"Alan": "Enlem", "Değer": f"{float(_mast.get('latitude')):.8f}" if _mast.get("latitude") is not None else "—"},
            {"Alan": "Boylam", "Değer": f"{float(_mast.get('longitude')):.8f}" if _mast.get("longitude") is not None else "—"},
            {"Alan": "UTM East", "Değer": _mast.get("utm_east") if _mast.get("utm_east") is not None else "—"},
            {"Alan": "UTM North", "Değer": _mast.get("utm_north") if _mast.get("utm_north") is not None else "—"},
            {"Alan": "UTM Zone", "Değer": _mast.get("utm_zone") or "—"},
        ])
        guvenli_dataframe(_konum, use_container_width=True, hide_index=True)

    st.markdown("#### Sensör yükseklikleri")
    _sensor_sirasi = ["WS1_Avg", "WS2_Avg", "WS3_Avg", "WS4_Avg", "WD1_Avg", "WD2_Avg"]
    _sensor_satirlari = [
        {"Sensör": _sensor, "Yükseklik": f"{float(_sensorler[_sensor]):g} m"}
        for _sensor in _sensor_sirasi if _sensor in _sensorler
    ]
    if _sensor_satirlari:
        _sensor_cols = st.columns(min(3, len(_sensor_satirlari)))
        for _i, _satir in enumerate(_sensor_satirlari):
            with _sensor_cols[_i % len(_sensor_cols)]:
                st.metric(_satir["Sensör"], _satir["Yükseklik"])
    else:
        st.info("Bu direk için onaylanmış sensör yüksekliği bulunmuyor.")

    if _veri_seti is not None and not _veri_seti.empty:
        st.markdown("#### Ölçüm verisi")
        _v1, _v2, _v3 = st.columns(3)
        _v1.metric("Başlangıç", _veri_seti["TIMESTAMP"].min().strftime("%d.%m.%Y %H:%M"))
        _v2.metric("Bitiş", _veri_seti["TIMESTAMP"].max().strftime("%d.%m.%Y %H:%M"))
        _v3.metric("Toplam kayıt", f"{len(_veri_seti):,}")

    _geri, _devam = st.columns([1, 2])
    with _geri:
        if st.button("← Kurulum raporuna dön", use_container_width=True, key="ozetten_rapora_v124"):
            st.session_state["ruzgar_olcumleri_adim_v112"] = 2
            app_state["measurement_step"] = 2
            st.rerun()
    with _devam:
        st.button(
            "Rüzgâr Kaynağı Özetine Geç →",
            type="primary",
            use_container_width=True,
            on_click=navigasyona_git,
            args=("Rüzgar Kaynağı Özeti",),
            key="olcum_ozetinden_analize_v124",
        )
    st.stop()

# Rüzgar Kaynağı Özeti doğrudan sidebar alt menüsünden açılır.

# ============================================================
# ANA SAYFA
# ============================================================

if sayfa == "Rüzgar Kaynağı Özeti":

    st.caption("Aylık istatistikler ve grafikler, yukarıda seçilen veri setini ve tarih aralığını kullanır.")
    _ozet_gorunum = st.radio("Veri görünümü", ["Ham Veri", "Temizlenmiş Veri"],
                             horizontal=True, key="ozet_veri_gorunumu_v11119")
    st.caption("Temizlenmiş veri: fiziksel sınır dışı ölçümler, kanıtla desteklenen otomatik kalite işaretleri ve manuel işaretler hariç tutulur. Tek başına sıfır ölçüm silinmez. Tahmini değerler ayrı tutulur.")
    ana_sayfa_dosya_adi = aktif_dosya_adi

    # Ölçüm güvenilirliği: ham, işaretlenmiş ve temizlenmiş kayıtlar ayrı tutulur.
    with st.container():
        st.subheader("Aylık Rüzgâr İstatistikleri")
        st.caption("Ham LoggerNet ölçümleri değiştirilmez. Temiz görünümde otomatik ve manuel kalite işaretli değerler boş kalır. Kalite gerekçeleri aşağıdaki raporda görülebilir; eksikler otomatik doldurulmaz.")
        _qc_mast = aktif_dosya_adi
        _qc_df = filtreli_veri.copy()
        _qc_df["TIMESTAMP"] = pd.to_datetime(_qc_df["TIMESTAMP"], errors="coerce")
        _qc_df = _qc_df.dropna(subset=["TIMESTAMP"]).sort_values("TIMESTAMP")
        _qc_sensors = hiz_sensor_kolonlari(_qc_df)
        if not _qc_sensors or _qc_df.empty:
            st.warning("Bu veri setinde geçerli zaman damgası veya hız sensörü bulunamadı.")
        else:
            _qc_sensor = st.selectbox("Sensör", _qc_sensors, key=f"qc_sensor_{_qc_mast}", format_func=lambda c: AKTIF_GORUNUR_ADLAR.get(c,c) if _qc_mast == aktif_dosya_adi else c)
            _qc_df[_qc_sensor] = pd.to_numeric(_qc_df[_qc_sensor], errors="coerce")
            _qc_key = "qc_flags_" + str(_qc_mast) + "_" + _qc_sensor
            if _qc_key not in st.session_state:
                st.session_state[_qc_key] = []
            _qc_flags = st.session_state[_qc_key]
            _qc_ts = _qc_df["TIMESTAMP"]
            _qc_v = _qc_df[_qc_sensor]
            _qc_invalid = _qc_v.isna() | ~np.isfinite(_qc_v) | (_qc_v < 0) | (_qc_v > 45)
            _qc_stuck = (_qc_v.rolling(6,min_periods=6).max() - _qc_v.rolling(6,min_periods=6).min() <= 0.01) & _qc_v.notna()
            _qc_peer = pd.Series(False,index=_qc_df.index)
            _qc_other = [c for c in _qc_sensors if c != _qc_sensor]
            if _qc_other:
                _qc_peer_median = _qc_df[_qc_other].apply(pd.to_numeric,errors="coerce").median(axis=1)
                _qc_peer = ((_qc_v - _qc_peer_median).abs() > 5) & _qc_peer_median.notna()
            _qc_suspicious = _qc_stuck | _qc_peer
            st.info(f"Otomatik ÖN İNCELEME: {_qc_invalid.sum():,} eksik/fiziksel sınır dışı; {_qc_stuck.sum():,} sabit-sensör şüphesi; {_qc_peer.sum():,} sensörler arası fark şüphesi. Şüpheli kayıtlar kendiliğinden silinmez.")
            _qc_stats_placeholder = st.empty()
            with st.expander("Sorunlu ölçümleri işaretle — tarih ve saat aralığı", expanded=False):
                st.caption(f"İşlem yapılacak sensör: {AKTIF_GORUNUR_ADLAR.get(_qc_sensor, _qc_sensor)} · {veri_seti_gorunur_adi(_qc_mast)}")
                for _date_name in ("start", "end"):
                    _date_key = f"qc_{_date_name}_{_qc_mast}_{_qc_sensor}"
                    _saved_date = st.session_state.get(_date_key)
                    if _saved_date is not None and not (_qc_ts.min().date() <= _saved_date <= _qc_ts.max().date()):
                        st.session_state[_date_key] = _qc_ts.min().date()
                _qc_col1,_qc_col2,_qc_col3=st.columns(3)
                with _qc_col1:
                    _qc_start=st.date_input("Başlangıç günü", value=_qc_ts.min().date(), min_value=_qc_ts.min().date(),max_value=_qc_ts.max().date(),key=f"qc_start_{_qc_mast}_{_qc_sensor}")
                    _qc_start_t=st.time_input("Başlangıç saati",value=datetime.time(0,0),key=f"qc_start_t_{_qc_mast}_{_qc_sensor}")
                with _qc_col2:
                    _qc_end=st.date_input("Bitiş günü",value=_qc_ts.min().date(),min_value=_qc_ts.min().date(),max_value=_qc_ts.max().date(),key=f"qc_end_{_qc_mast}_{_qc_sensor}")
                    _qc_end_t=st.time_input("Bitiş saati",value=datetime.time(23,59),key=f"qc_end_t_{_qc_mast}_{_qc_sensor}")
                with _qc_col3:
                    _qc_reason=st.selectbox("Sorun türü",["Düşük ölçüm kalitesi","Buzlanma şüphesi","Direk gölgelemesi","Kullanıcı tarafından hariç tutma"],key=f"qc_reason_{_qc_mast}_{_qc_sensor}")
                    _qc_apply=st.button("Seçilen sensörün ölçümlerini hariç tut",key=f"qc_apply_{_qc_mast}_{_qc_sensor}")
                _qc_from=pd.Timestamp(datetime.datetime.combine(_qc_start,_qc_start_t))
                _qc_to=pd.Timestamp(datetime.datetime.combine(_qc_end,_qc_end_t))
                if _qc_apply:
                    if _qc_to < _qc_from:
                        st.error("Bitiş tarihi başlangıçtan önce olamaz.")
                    else:
                        _qc_count=int(((_qc_ts>=_qc_from)&(_qc_ts<=_qc_to)).sum())
                        if _qc_count:
                            _qc_flags.append({"from":str(_qc_from),"to":str(_qc_to),"reason":_qc_reason,"count":_qc_count})
                            st.success(f"{_qc_count} kayıt için {_qc_reason} işareti eklendi.")
                        else:
                            st.warning("Bu aralıkta kayıt yok.")
                _qc_manual=pd.Series(False,index=_qc_df.index)
                for _qc_f in _qc_flags:
                    _qc_manual |= (_qc_ts>=pd.Timestamp(_qc_f["from"])) & (_qc_ts<=pd.Timestamp(_qc_f["to"]))
                if _qc_flags:
                    st.dataframe(pd.DataFrame(_qc_flags).rename(columns={"from":"Başlangıç", "to":"Bitiş", "reason":"Sorun türü", "count":"İşaretli kayıt"}),use_container_width=True,hide_index=True)
                    if st.button("Bu sensörün kalite işaretlerini geri al",key=f"qc_undo_{_qc_mast}_{_qc_sensor}"):
                        st.session_state[_qc_key]=[]
                        _qc_flags=[]
                        _qc_manual=pd.Series(False,index=_qc_df.index)
                        st.success("Kalite işaretleri geri alındı.")
            with _qc_stats_placeholder.container():
                _qc_usable = (_qc_v.replace([np.inf, -np.inf], np.nan)
                              if _ozet_gorunum == "Ham Veri"
                              else olcum_kalite_verisi(_qc_df, _qc_mast)[_qc_sensor])
                _qc_table=_qc_monthly_table(_qc_ts,_qc_v,_qc_usable)
                _qc_month_names = {1:"Ocak",2:"Şubat",3:"Mart",4:"Nisan",5:"Mayıs",6:"Haziran",7:"Temmuz",8:"Ağustos",9:"Eylül",10:"Ekim",11:"Kasım",12:"Aralık"}
                _qc_display = _qc_table.drop(columns=["Beklenen kayıt (dönem)","Mevcut kayıt","Geçerli kayıt","DCR (%)","DRR (%)"],errors="ignore").copy()
                _qc_display["Ay"] = _qc_display["Ay"].map(_qc_month_names)
                _qc_display = _qc_display.rename(columns={"Ortalama (m/s)":"ORTALAMA HIZ (m/s)"})
                st.dataframe(_qc_display.style.format({"ORTALAMA HIZ (m/s)":"{:.3f}","Medyan (m/s)":"{:.3f}","Min (m/s)":"{:.3f}","Maks (m/s)":"{:.3f}","Std. sapma (m/s)":"{:.3f}"},na_rep="—").set_properties(subset=["ORTALAMA HIZ (m/s)"],**{"background-color":"#DCEFE9","color":"#075E53","font-weight":"bold"}),use_container_width=True,hide_index=True)
                st.download_button("Aylık istatistikleri CSV indir",_qc_display.to_csv(index=False).encode("utf-8-sig"),file_name="qc_aylik_istatistik.csv",mime="text/csv",key="qc_download")
            _qc_flag_export=pd.DataFrame(_qc_flags)
            st.download_button("Kalite işaretlerini CSV indir",_qc_flag_export.to_csv(index=False).encode("utf-8-sig"),file_name="qc_manuel_bayraklar.csv",mime="text/csv",key="qc_flags_export")
            with st.expander("Windographer ile doğrulama", expanded=False):
                _qc_ref_file=st.file_uploader("Windographer Monthly Statistics TXT / TSV yükle",type=["txt","tsv","csv"],key="qc_ref")
                if _qc_ref_file is not None:
                    try:
                        _qc_ref=_qc_read_windographer(_qc_ref_file.getvalue())
                        _qc_cmp=_qc_table.merge(_qc_ref,on=["Yıl","Ay"],how="outer",indicator=True)
                        _qc_cmp["Ortalama farkı (m/s)"]=_qc_cmp["Ortalama (m/s)"]-_qc_cmp["WG Ortalama (m/s)"]
                        _qc_cmp["Kayıt farkı"]=_qc_cmp["Geçerli kayıt"]-_qc_cmp["WG Valid"]
                        st.dataframe(_qc_cmp,use_container_width=True,hide_index=True)
                        st.download_button("Karşılaştırma raporunu indir",_qc_cmp.to_csv(index=False).encode("utf-8-sig"),file_name="windographer_dogrulama.csv",mime="text/csv",key="qc_cmp_download")
                        _qc_bad=(_qc_cmp["Ortalama farkı (m/s)"].abs()>0.00051)|(_qc_cmp["Kayıt farkı"]!=0)|(_qc_cmp["Beklenen kayıt (dönem)"]!=_qc_cmp["WG Possible"])|(_qc_cmp["_merge"]!="both")
                        if bool(_qc_bad.any()):
                            st.error(f"UYUMSUZLUK: {int(_qc_bad.sum())} ayda ortalama, kayıt veya dönem farkı var. Bu veri için doğrulama ONAYLANMADI.")
                        else:
                            st.success("Yüklenen referansla aylık ortalama ve mevcut kayıt sayıları yuvarlama toleransı içinde eşleşiyor. Diğer kalite kontrol kuralları ayrıca doğrulanmalıdır.")
                    except Exception as _qc_exc:
                        st.error(f"Referans dosyası okunamadı: {_qc_exc}")
            st.caption("Kalite işaretleri bu proje sekmesi için saklanır. Enerji hesabı bu işaretleri otomatik uygular; ayrıca kullanıcı onayı gerekmez.")

    with st.expander("Sensörler arası düşük ölçüm incelemesi", expanded=False):
        st.caption("Üst sensörün düşük ölçmesi tek başına arıza kanıtı değildir. Bu tablo aynı zamanlardaki ölçümleri yıl ve ayı ayırarak karşılaştırır; değerleri değiştirmez.")
        _diag_sensors = [c for c in RUZGAR_KOLONLARI if c in filtreli_veri and float(aktif_yukseklikler.get(c, 0) or 0)>0]
        _diag_sensors.sort(key=lambda c: float(aktif_yukseklikler[c]), reverse=True)
        if len(_diag_sensors) >= 2:
            _diag_upper = _diag_sensors[0]
            _diag_lowers = [c for c in _diag_sensors[1:] if float(aktif_yukseklikler[c]) < float(aktif_yukseklikler[_diag_upper])]
            if _diag_lowers:
                _diag_lower = st.selectbox("Alt referans sensörü", _diag_lowers, format_func=lambda c: AKTIF_GORUNUR_ADLAR.get(c,c), key=f"diag_lower_{aktif_dosya_adi}")
                st.write(f"Üst sensör: **{AKTIF_GORUNUR_ADLAR[_diag_upper]}**")
                _diag_source = filtreli_veri if _ozet_gorunum == "Ham Veri" else olcum_kalite_verisi(filtreli_veri, aktif_dosya_adi)
                _diag = sensor_donem_incelemesi(_diag_source, _diag_upper, _diag_lower)
                st.dataframe(_diag, hide_index=True, use_container_width=True)
                st.download_button("Sensör incelemesini CSV indir", _diag.to_csv(index=False).encode("utf-8-sig"), file_name="sensor_donem_incelemesi.csv", mime="text/csv")
                st.caption("Eksik kayıt dönemleri, sensör bağlantısı/kalibrasyonu, direk gölgelemesi ve hava koşulları birlikte incelenmelidir. Buzlanma kararı için sıcaklık ve zaman serisi gibi ek kanıt gerekir.")
        else:
            st.info("İnceleme için yükseklikleri tanımlı en az iki hız sensörü gereklidir.")

    _review_clean, _review_ref, _coverage_table, _coverage_status = enerji_kalite_durumu(filtreli_veri, aktif_dosya_adi, aktif_yukseklikler)
    with st.expander("Yüklenen bütün dosyaların ön kontrol özeti", expanded=False):
        st.dataframe(pd.DataFrame(tum_dosya_kalite_ozeti), hide_index=True, use_container_width=True)
        st.caption("Aynı motor bütün yüklenen dosyalara uygulanır. Sensör sayısı çapraz kontrol için yetersizse sıfır/sabit ölçüm otomatik arıza sayılmaz; manuel inceleme gerekir.")
    with st.expander("Veri kalitesi ve enerjiye uygunluk raporu", expanded=True):
        _auto_mask, _auto_reason, _auto_events, _timing = otomatik_olcum_kontrolu(tum_veri_setleri[aktif_dosya_adi])
        if not _auto_events.empty:
            _visible_events = _auto_events[(_auto_events["Bitiş"] >= pd.Timestamp(baslangic_tarihi)) & (_auto_events["Başlangıç"] < pd.Timestamp(bitis_tarihi)+pd.Timedelta(days=1))]
            st.warning(f"Seçilen dönemde {len(_visible_events)} otomatik sensör kalite işareti var. Temiz görünüm ve enerji hesabında bu ölçümler dışlanır.")
            st.dataframe(_visible_events, hide_index=True, use_container_width=True)
        else:
            st.caption("Uzun sıfır/sabit sensör kuralı bu dosyada desteklenen bir olay bulmadı. Bu sonuç, tüm ölçümlerin doğru olduğunu kanıtlamaz.")
        st.caption("Otomatik kurallar: 0–45 m/s fiziksel aralık; en az 6 kayıt ve 1 saat sıfıra yakın (≤0,25 m/s) veya sabit ölçüm; aynı sürenin en az %80'inde iki başka sensörün >2 m/s ölçmesi. Sabitlikte diğer iki sensörün değişimi de kontrol edilir. Bunlar uygulama içi tarama eşikleridir; otomatik arıza teşhisi değildir.")
        if not _timing["cadence_ok"] or _timing["duplicates"]:
            st.error(f"Zaman ekseni kontrolü başarısız: {_timing['duplicates']} yinelenen zaman damgası. Düzenli kayıt aralığı belirlenmeden enerji hesabı açılmaz.")
        if _review_ref is None:
            st.info("Enerji için ölçülen hız kanallarının sensör yüksekliklerini girin.")
        else:
            st.caption(f"Enerji referansı: {AKTIF_GORUNUR_ADLAR.get(_review_ref,_review_ref)} · Kayıt aralığı: {_coverage_status.get('step_seconds',float('nan'))/60:g} dakika")
            if not _coverage_table.empty:
                st.dataframe(_coverage_table, hide_index=True, use_container_width=True)
                st.download_button("Kalite ve veri kapsamı raporunu CSV indir", _coverage_table.to_csv(index=False).encode("utf-8-sig"), file_name="veri_kalite_kapsami.csv", mime="text/csv")
            if _coverage_status["annual_ok"]:
                st.info("Yıllık ön tahmin için veri kapsamı kontrolü geçti. Bu bir ölçüm sertifikası veya P50/P90 doğrulaması değildir.")
            else:
                st.warning("Bu dönem için yıllık üretim gösterilmez: en az 365 günlük kayıt, her ay en az %90 geçerli ölçüm ve en fazla 2 saatlik tek boşluk koşulları birlikte sağlanmalı. Bunlar uygulamanın ihtiyatlı iç kontrol eşikleridir.")
                if np.isfinite(_coverage_status.get("longest_gap_hours",np.nan)):
                    st.write(f"En uzun eksik / dışlanan dönem: {_coverage_status['longest_gap_hours']:.1f} saat")

    with st.expander("Eksik veri tamamlama · yöntem testi", expanded=False):
        st.caption("Model her direğin kendi sağlam ölçümlerinden kurulur. Seçilen hedef sensörü ardışık zaman bloklarında gizleyerek tahmin hatası ölçülür. Aday tahminler ayrı dosyaya çıkarılır; enerjiye otomatik aktarılmaz. Hız hatasının küçük olması, enerji hatasının küçük olduğunu tek başına kanıtlamaz.")
        _model_sensors = hiz_sensor_kolonlari(filtreli_veri)
        if len(_model_sensors) >= 2:
            _model_target = st.selectbox("Tamamlanacak sensör", _model_sensors, key=f"fill_target_{aktif_dosya_adi}", format_func=lambda c:AKTIF_GORUNUR_ADLAR.get(c,c))
            _reference_options = [c for c in _model_sensors if c != _model_target]
            _reference_options.sort(key=lambda c:int(_review_clean.loc[_review_clean[_model_target].isna(),c].notna().sum()), reverse=True)
            _model_ref = st.selectbox("Sağlam referans sensörü", _reference_options, key=f"fill_reference_{aktif_dosya_adi}", format_func=lambda c:AKTIF_GORUNUR_ADLAR.get(c,c))
            _model_days = st.number_input("Test boşluğu uzunluğu (gün)", min_value=1, max_value=120, value=int(max(7,min(120,math.ceil(_coverage_status.get("longest_gap_hours",0)/24)))) if np.isfinite(_coverage_status.get("longest_gap_hours",np.nan)) else 7, key=f"fill_days_{aktif_dosya_adi}")
            _curve_options = {f"{_manufacturer} / {_name}":_details["power_curve"] for _manufacturer,_models in TURBIN_KUTUPHANESI.items() for _name,_details in _models.items()}
            _test_curve_name = st.selectbox("Test için türbin güç eğrisi", list(_curve_options), key=f"fill_curve_{aktif_dosya_adi}")
            st.caption("Enerji sapması testi hedef sensör yüksekliğindeki hızlarla yapılır; türbin göbek yüksekliği veya hava yoğunluğu dönüşümünü doğrulamaz.")
            if st.button("Sağlam dönemlerde yöntemi test et", key=f"fill_test_{aktif_dosya_adi}"):
                _full_clean = olcum_kalite_verisi(tum_veri_setleri[aktif_dosya_adi], aktif_dosya_adi)
                _test_result, _fit = tamamlama_blok_testi(_full_clean, _model_target, _model_ref, int(_model_days), _curve_options[_test_curve_name])
                if _test_result.empty:
                    st.info("Bağımsız zaman bloklarını test etmek için yeterli ortak sağlam ölçüm yok.")
                else:
                    st.dataframe(_test_result, hide_index=True, use_container_width=True)
                    st.download_button("Tamamlama test raporunu indir", _test_result.to_csv(index=False).encode("utf-8-sig"), file_name="tamamlama_blok_testi.csv", mime="text/csv")
                if _fit is not None:
                    _candidate = tamamlama_aday_verisi(_full_clean, _model_target, _model_ref, _fit)
                    st.download_button("Tahmini aday veriyi ayrı CSV indir", _candidate.to_csv(index=False).encode("utf-8-sig"), file_name="tamamlama_aday_verisi.csv", mime="text/csv")
                    st.caption("CSV'deki Kaynak sütunu gerçek ölçüm, eksik ve tahmini adayı ayırır. Hedef sensörün özgün arızalı ölçümü ham dosyada korunur.")
        else:
            st.info("Tamamlama testi için en az iki hız sensörü gereklidir.")

    kalite_isaretlerini_sakla()
    st.markdown("#### Sonraki adım · Enerji analizi")
    st.caption("Enerji sayfasına doğrudan geçebilirsiniz. Hesaplarda gerçek temiz ölçümler kullanılır; eksik değerler doldurulmaz. Yıllık sonuç veri kapsamı koşullarına bağlıdır.")
    st.button("Enerji hesabına geç →", type="primary", key="energy_continue_v111119",
              on_click=navigasyona_git, args=("Üretim Hesaplama",))

    ana_sayfa_verisi = (filtreli_veri.copy() if _ozet_gorunum == "Ham Veri"
                        else olcum_kalite_verisi(filtreli_veri, aktif_dosya_adi))
    with st.expander("Rüzgâr grafikleri ve yükseklik profili", expanded=False):
        st.markdown("---")

        # --------------------------------------------------------
        # Ortalama kartları
        # --------------------------------------------------------

        kart1, kart2, kart3, kart4, kart5 = st.columns(5)

        kart1.metric(
            f"{AKTIF_GORUNUR_ADLAR['WS1_Avg']} ortalama",
            f"{ana_sayfa_verisi['WS1_Avg'].mean():.2f} m/s"
        )

        kart2.metric(
            f"{AKTIF_GORUNUR_ADLAR['WS2_Avg']} ortalama",
            f"{ana_sayfa_verisi['WS2_Avg'].mean():.2f} m/s"
        )

        kart3.metric(
            f"{AKTIF_GORUNUR_ADLAR['WS3_Avg']} ortalama",
            f"{ana_sayfa_verisi['WS3_Avg'].mean():.2f} m/s"
        )

        kart4.metric(
            f"{AKTIF_GORUNUR_ADLAR['WS4_Avg']} ortalama",
            f"{ana_sayfa_verisi['WS4_Avg'].mean():.2f} m/s"
        )

        with kart5:
            # Kartı diğer dört sensör kartıyla aynı üst hizaya yerleştirmek için
            # mevcut widget değeriyle sonuç önce çizilir; giriş alanı kartın altında kalır.
            _manuel_h = float(st.session_state.get("manuel_hedef_yukseklik_v127", 100.0))
            _manuel_sonuc = hedef_yukseklik_ortalama_hizi_hesapla(
                ana_sayfa_verisi,
                aktif_yukseklikler,
                _manuel_h,
            )
            if _manuel_sonuc.get("ok"):
                st.metric(
                    f"{_manuel_h:g} m tahmini ortalama",
                    f"{_manuel_sonuc['hiz']:.2f} m/s",
                )
            else:
                st.metric(f"{_manuel_h:g} m tahmini ortalama", "—")

            st.number_input(
                "Manuel yükseklik (m)",
                min_value=1.0,
                max_value=300.0,
                value=_manuel_h,
                step=1.0,
                key="manuel_hedef_yukseklik_v127",
                help="Ölçüm aralığında komşu sensörler arası log-log enterpolasyon; aralık dışında tüm sensörlerle power-law ekstrapolasyonu uygulanır.",
            )

            if _manuel_sonuc.get("ok"):
                _detay = f"{_manuel_sonuc['yontem']} · {_manuel_sonuc['kayit']:,} eşzamanlı kayıt"
                if _manuel_sonuc.get("alpha") is not None:
                    _detay += f" · α={_manuel_sonuc['alpha']:.4f}"
                if _manuel_sonuc.get("r2") is not None and _manuel_sonuc.get("tur") == "ekstrapolasyon":
                    _detay += f" · R²={_manuel_sonuc['r2']:.3f}"
                st.caption(_detay)
                if _manuel_sonuc.get("tur") == "ekstrapolasyon":
                    st.warning(
                        f"Hedef yükseklik ölçüm aralığının ({_manuel_sonuc['alt_h']:g}–{_manuel_sonuc['ust_h']:g} m) dışındadır; sonuç ekstrapolasyondur."
                    )
            else:
                st.warning(_manuel_sonuc.get("mesaj", "Hesap yapılamadı."))
        sol_ust, sag_ust = st.columns(2)

        # --------------------------------------------------------
        # Hâkim rüzgar yönü / Wind Direction Frequency
        # WD1_Avg = 83 m, WD2_Avg = 78.5 m
        # --------------------------------------------------------

        with sol_ust:
            st.subheader("Wind Direction Frequency")

            _aktif_rapor = veri_seti_mast_kaydi(aktif_dosya_adi) or {}
            _wd_yuk = (_aktif_rapor.get("sensors", {}) or {})
            _bulunan_yon_hiz_ciftleri = _yon_hiz_kolon_ciftleri_bul(ana_sayfa_verisi, _wd_yuk)
            yon_sensorleri = {}
            for _etiket, _yon_kol, _hiz_kol in _bulunan_yon_hiz_ciftleri:
                _no = _kolon_sira_no(_yon_kol)
                _rapor_anahtari = f"WD{_no}_Avg" if _no in (1, 2) else None
                _h = float(_wd_yuk.get(_rapor_anahtari, 0.0) or 0.0) if _rapor_anahtari else 0.0
                _gorunen = f"{_yon_kol} ({_h:g} m)" if _h > 0 else str(_yon_kol)
                yon_sensorleri[_gorunen] = {"yon": _yon_kol, "hiz": _hiz_kol}

            # Windographer benzeri 22.5 derece sektörler
            sektor_genisligi = 22.5
            sektor_merkezleri = np.arange(
                0,
                360,
                sektor_genisligi
            )

            # Çok düşük hızlarda yön ölçümü anlamlı olmayabilir.
            # Gerekirse bu değeri değiştirebilirsin.
            minimum_hiz = 0.5

            yon_fig = go.Figure()
            bulunan_sensor_sayisi = 0

            for sensor_adi, kolonlar in yon_sensorleri.items():

                yon_kolonu = kolonlar["yon"]
                hiz_kolonu = kolonlar["hiz"]

                if (
                    yon_kolonu not in ana_sayfa_verisi.columns
                    or hiz_kolonu not in ana_sayfa_verisi.columns
                ):
                    continue

                yon_verisi = ana_sayfa_verisi[
                    [yon_kolonu, hiz_kolonu]
                ].copy()

                # Geçersiz yön ve hızları çıkar
                yon_verisi = yon_verisi[
                    yon_verisi[yon_kolonu].notna()
                    & yon_verisi[hiz_kolonu].notna()
                    & (yon_verisi[yon_kolonu] >= 0)
                    & (yon_verisi[yon_kolonu] < 360)
                    & (yon_verisi[hiz_kolonu] >= minimum_hiz)
                    & (yon_verisi[hiz_kolonu] <= 45)
                ]

                if yon_verisi.empty:
                    continue

                # Her yönü en yakın 22.5 derece sektör merkezine ata
                yon_verisi["Yön Grubu"] = (
                    np.floor(
                        (
                            yon_verisi[yon_kolonu]
                            + sektor_genisligi / 2
                        )
                        / sektor_genisligi
                    )
                    * sektor_genisligi
                ) % 360

                yon_ozeti = (
                    yon_verisi
                    .groupby("Yön Grubu")
                    .size()
                    .reindex(
                        sektor_merkezleri,
                        fill_value=0
                    )
                )

                yon_orani = (
                    yon_ozeti
                    / yon_ozeti.sum()
                    * 100
                )

                # Polar çizgiyi kapatmak için ilk noktayı sona ekle
                theta = list(sektor_merkezleri) + [
                    sektor_merkezleri[0]
                ]

                r_degerleri = list(
                    yon_orani.to_numpy()
                ) + [
                    yon_orani.iloc[0]
                ]

                yon_fig.add_trace(
                    go.Barpolar(
                        r=list(yon_orani.to_numpy()),
                        theta=list(sektor_merkezleri),
                        width=[sektor_genisligi * 0.88] * len(sektor_merkezleri),
                        name=sensor_adi,
                        opacity=0.68,
                        hovertemplate=(
                            f"{sensor_adi}<br>"
                            "Yön: %{theta:.1f}°<br>"
                            "Frekans: %{r:.2f}%"
                            "<extra></extra>"
                        )
                    )
                )

                bulunan_sensor_sayisi += 1

            if bulunan_sensor_sayisi == 0:
                _yon_aday = [
                    k for k in ana_sayfa_verisi.columns
                    if (
                        _kolon_adi_norm(k).startswith(("wd", "winddir", "direction", "dir"))
                        or "winddirection" in _kolon_adi_norm(k)
                    )
                ]
                if _yon_aday:
                    st.warning(
                        "Rüzgâr yönü kolonu bulundu ancak geçerli yön-hız eşzamanlı kaydı "
                        "oluşturulamadı. Yön kolonları: " + ", ".join(map(str, _yon_aday))
                    )
                else:
                    st.warning(
                        "WindData dosyasında rüzgâr yönü kolonu bulunamadı. "
                        "WD, WindDir veya WindDirection isimli bir yön kolonu bekleniyor."
                    )

            else:
            
                yon_fig.update_layout(
        polar=dict(
            bgcolor="white",

            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickmode="array",
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                ticktext=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                gridcolor="lightgray",
                linecolor="gray"
            ),

            radialaxis=dict(
                visible=True,
                ticksuffix="%",
                showline=False,
                gridcolor="lightgray",
                tickfont=dict(size=11)
            )
        ),

        showlegend=True,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5
        ),

        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40
        ),

        height=400
    )
                st.plotly_chart(
                    yon_fig,
                    use_container_width=True,
                    config={
                        "displaylogo": False,
                        "scrollZoom": False
                    }
                )
                      
        # --------------------------------------------------------
        # Vertical wind shear profile
        # --------------------------------------------------------

        with sag_ust:
            st.subheader("Vertical Wind Shear Profile")

            # Windographer benzeri hesap:
            # 1) Dört sensörün aynı anda geçerli olduğu kayıtlar kullanılır.
            # 2) Bu eşzamanlı kayıtların her yükseklikteki ortalaması alınır.
            # 3) V = A * H^alpha güç yasası log-log regresyon ile uydurulur.
            sensor_sirasi_tumu = ["WS4_Avg", "WS3_Avg", "WS2_Avg", "WS1_Avg"]
            # Yalnız kurulum raporunda geçerli (>0) yüksekliği olan sensörler kullanılır.
            sensor_sirasi = [
                k for k in sensor_sirasi_tumu
                if k in ana_sayfa_verisi.columns
                and np.isfinite(float(aktif_yukseklikler.get(k, 0.0) or 0.0))
                and float(aktif_yukseklikler.get(k, 0.0) or 0.0) > 0
            ]
            yukseklikler = np.array(
                [float(aktif_yukseklikler[k]) for k in sensor_sirasi], dtype=float
            )

            shear_veri = ana_sayfa_verisi[sensor_sirasi].copy()
            shear_veri = shear_veri.replace([np.inf, -np.inf], np.nan)

            for kolon in sensor_sirasi:
                shear_veri.loc[
                    (shear_veri[kolon] <= 0)
                    | (shear_veri[kolon] > 45),
                    kolon
                ] = np.nan

            # Geçerli yüksekliği bulunan sensörlerin aynı anda geçerli olduğu satırlar.
            shear_eszamanli = shear_veri.dropna(subset=sensor_sirasi) if sensor_sirasi else pd.DataFrame()

            if len(sensor_sirasi) < 2:
                st.warning(
                    "Dikey shear hesabı için en az iki geçerli WS sensör yüksekliği bulunmalıdır. "
                    "Kurulum raporu kaydı ve aktif veri seti eşleştirmesi kontrol ediliyor."
                )
                st.caption(
                    "Aktif eşleştirme: "
                    + ", ".join(
                        f"{k}={float(aktif_yukseklikler.get(k, 0.0) or 0.0):g} m"
                        for k in RUZGAR_KOLONLARI
                    )
                )
            elif shear_eszamanli.empty:
                st.warning(
                    "Geçerli yüksekliği olan sensörlerin aynı anda ölçüm yaptığı kayıt bulunamadı."
                )
            else:
                ortalama_hizlar = (
                    shear_eszamanli[sensor_sirasi]
                    .mean(axis=0)
                    .to_numpy(dtype=float)
                )

                gecerli_noktalar = (
                    np.isfinite(ortalama_hizlar)
                    & (ortalama_hizlar > 0)
                )

                x_log = np.log(yukseklikler[gecerli_noktalar])
                y_log = np.log(ortalama_hizlar[gecerli_noktalar])
                if (
                    gecerli_noktalar.sum() < 2
                    or len(np.unique(np.round(x_log, 10))) < 2
                ):
                    st.warning(
                        "Power-law regresyonu için en az iki farklı ve geçerli sensör yüksekliği gerekli."
                    )
                else:
                    try:
                        alpha, log_a = np.polyfit(x_log, y_log, 1)
                    except (np.linalg.LinAlgError, ValueError, FloatingPointError):
                        alpha, log_a = np.nan, np.nan
                    if not (np.isfinite(alpha) and np.isfinite(log_a)):
                        st.warning("Shear regresyonu hesaplanamadı; sensör yüksekliği ve veri uygunluğu kontrol edilmeli.")
                        alpha, log_a = 0.14, np.log(max(float(np.nanmean(ortalama_hizlar)), 0.01))
                    a_katsayisi = float(np.exp(log_a))

                    # Eğriyi sensörlerin ve manuel hedef noktanın tamamını kapsayacak şekilde çiz.
                    _profil_min_h = float(yukseklikler.min())
                    _profil_max_h = float(yukseklikler.max())
                    if _manuel_sonuc.get("ok"):
                        _profil_min_h = min(_profil_min_h, float(_manuel_h))
                        _profil_max_h = max(_profil_max_h, float(_manuel_h))
                    egri_yukseklik = np.linspace(
                        max(1.0, _profil_min_h - 10.0),
                        _profil_max_h + 10.0,
                        300,
                    )
                    egri_hiz = a_katsayisi * np.power(
                        egri_yukseklik,
                        alpha
                    )

                    profil_fig = go.Figure()

                    profil_fig.add_trace(
                        go.Scatter(
                            x=egri_hiz,
                            y=egri_yukseklik,
                            mode="lines",
                            name=f"Power law (alpha = {alpha:.3f})",
                            line=dict(width=2.5),
                            hovertemplate=(
                                "Height: %{y:.1f} m<br>"
                                "Wind speed: %{x:.2f} m/s<extra></extra>"
                            )
                        )
                    )

                    profil_fig.add_trace(
                        go.Scatter(
                            x=ortalama_hizlar,
                            y=yukseklikler,
                            mode="markers+text",
                            name="Sensor means",
                            text=[AKTIF_GORUNUR_ADLAR[k] for k in sensor_sirasi],
                            textposition="middle right",
                            marker=dict(
                                symbol="diamond",
                                size=9,
                                line=dict(width=1)
                            ),
                            hovertemplate=(
                                "%{text}<br>"
                                "Mean wind speed: %{x:.3f} m/s"
                                "<extra></extra>"
                            )
                        )
                    )

                    # Kullanıcının girdiği hedef yüksekliği farklı renkte ve belirgin bir yıldızla göster.
                    if _manuel_sonuc.get("ok"):
                        profil_fig.add_trace(
                            go.Scatter(
                                x=[float(_manuel_sonuc["hiz"])],
                                y=[float(_manuel_h)],
                                mode="markers+text",
                                name="User-defined Height",
                                text=[f"User-defined {_manuel_h:g} m"],
                                textposition="middle left",
                                marker=dict(
                                    symbol="square-cross",
                                    size=15,
                                    color="#f4a321",
                                    line=dict(color="#9a5b00", width=1.5),
                                ),
                                hovertemplate=(
                                    "User-defined Height<br>"
                                    "Height: %{y:.2f} m<br>"
                                    "Estimated mean wind speed: %{x:.3f} m/s"
                                    "<extra></extra>"
                                ),
                            )
                        )

                    _x_degerleri = np.r_[egri_hiz, ortalama_hizlar]
                    if _manuel_sonuc.get("ok"):
                        _x_degerleri = np.r_[_x_degerleri, float(_manuel_sonuc["hiz"])]
                    x_alt = float(np.nanmin(_x_degerleri))
                    x_ust = float(np.nanmax(_x_degerleri))
                    x_bosluk = max((x_ust - x_alt) * 0.20, 0.25)

                    profil_fig.update_layout(
                        xaxis=dict(
                            title="Mean Wind Speed (m/s)",
                            range=[max(0, x_alt - x_bosluk), x_ust + x_bosluk],
                            fixedrange=True,
                            showgrid=True,
                            zeroline=False
                        ),
                        yaxis=dict(
                            title="Height Above Ground (m)",
                            range=[max(0.0, _profil_min_h - 10.0), _profil_max_h + 10.0],
                            dtick=10,
                            fixedrange=True,
                            showgrid=True,
                            zeroline=False
                        ),
                        legend=dict(
                            x=0.02,
                            y=0.98,
                            xanchor="left",
                            yanchor="top",
                            bgcolor="rgba(255,255,255,0.90)",
                            bordercolor="black",
                            borderwidth=1
                        ),
                        margin=dict(l=60, r=35, t=20, b=50),
                        height=420,
                        dragmode=False,
                        hovermode="closest"
                    )

                    st.plotly_chart(
                        profil_fig,
                        use_container_width=True,
                        config={
                            "scrollZoom": False,
                            "displaylogo": False,
                            "modeBarButtonsToRemove": [
                                "zoom2d", "pan2d", "select2d", "lasso2d",
                                "zoomIn2d", "zoomOut2d", "autoScale2d",
                                "resetScale2d"
                            ]
                        }
                    )

                    st.caption(
                        f"V = {a_katsayisi:.4f} × H^{alpha:.4f} | "
                        f"Eşzamanlı geçerli kayıt: {len(shear_eszamanli):,}"
                    )

        sol_alt, sag_alt = st.columns(2)

        # --------------------------------------------------------
        # Monthly mean wind speed
        # --------------------------------------------------------

        with sol_alt:
            baslik_col, yil_col = st.columns([3, 1])

            with baslik_col:
                st.subheader("Monthly Mean Wind Speed")

            mevcut_yillar = sorted(
                ana_sayfa_verisi["TIMESTAMP"]
                .dt.year
                .dropna()
                .astype(int)
                .unique()
                .tolist()
            )

            with yil_col:
                secilen_yil = st.selectbox(
                    "Yıl",
                    ["Tüm Yıllar"] + mevcut_yillar,
                    key="monthly_yil_secimi"
                )

            # Seçilen veri katmanı kullanılır; yeniden filtreleme/tamamlama yapılmaz.
            aylik_veri = ana_sayfa_verisi[
                ["TIMESTAMP"] + RUZGAR_KOLONLARI
            ].copy()
            aylik_veri = aylik_veri.replace([np.inf, -np.inf], np.nan)

            if secilen_yil != "Tüm Yıllar":
                aylik_veri = aylik_veri[
                    aylik_veri["TIMESTAMP"].dt.year == int(secilen_yil)
                ]

            aylik_veri["Ay"] = aylik_veri["TIMESTAMP"].dt.month

            # Tüm yıllar seçiliyken aynı takvim ayları birlikte ortalanır.
            aylik = (
                aylik_veri
                .groupby("Ay", observed=False)[RUZGAR_KOLONLARI]
                .mean()
                .reindex(range(1, 13))
                .rename(columns=AKTIF_GORUNUR_ADLAR)
                .reset_index()
            )

            ay_adlari = [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]
            aylik["Ay Adı"] = aylik["Ay"].map(
                dict(enumerate(ay_adlari, start=1))
            )

            aylik_uzun = aylik.melt(
                id_vars=["Ay", "Ay Adı"],
                value_vars=[AKTIF_GORUNUR_ADLAR[k] for k in RUZGAR_KOLONLARI],
                var_name="Sensör",
                value_name="Rüzgar Hızı"
            )

            aylik_fig = px.line(
                aylik_uzun,
                x="Ay Adı",
                y="Rüzgar Hızı",
                color="Sensör",
                color_discrete_map={
                    AKTIF_GORUNUR_ADLAR["WS1_Avg"]: "#0875D1",
                    AKTIF_GORUNUR_ADLAR["WS2_Avg"]: "#69B9FF",
                    AKTIF_GORUNUR_ADLAR["WS3_Avg"]: "#FF2B2B",
                    AKTIF_GORUNUR_ADLAR["WS4_Avg"]: "#FF9C9C",
                },
                markers=True,
                category_orders={
                    "Ay Adı": ay_adlari,
                    "Sensör": [AKTIF_GORUNUR_ADLAR[k] for k in RUZGAR_KOLONLARI]
                },
                labels={
                    "Ay Adı": "",
                    "Rüzgar Hızı": "Mean Wind Speed (m/s)"
                }
            )

            aylik_fig.update_traces(
                marker=dict(symbol="diamond", size=7),
                line=dict(width=2.2),
                connectgaps=False,
                hovertemplate=(
                    "%{fullData.name}<br>"
                    "%{x}: %{y:.3f} m/s<extra></extra>"
                )
            )

            aylik_degerler = aylik_uzun["Rüzgar Hızı"].dropna()
            if aylik_degerler.empty:
                y_min, y_max = 0.0, 8.0
            else:
                alt = float(aylik_degerler.min())
                ust = float(aylik_degerler.max())
                bosluk = max((ust - alt) * 0.20, 0.30)
                y_min = max(0.0, np.floor((alt - bosluk) * 2) / 2)
                y_max = np.ceil((ust + bosluk) * 2) / 2
                if y_max <= y_min:
                    y_max = y_min + 1.0

            aylik_fig.update_layout(
                xaxis=dict(
                    type="category",
                    categoryorder="array",
                    categoryarray=ay_adlari,
                    tickmode="array",
                    tickvals=ay_adlari,
                    ticktext=ay_adlari,
                    fixedrange=True,
                    showgrid=True,
                    zeroline=False
                ),
                yaxis=dict(
                    title="Mean Wind Speed (m/s)",
                    range=[y_min, y_max],
                    dtick=0.5,
                    fixedrange=True,
                    showgrid=True,
                    zeroline=False
                ),
                legend=dict(
                    x=0.02,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="rgba(255,255,255,0.90)",
                    bordercolor="black",
                    borderwidth=1
                ),
                margin=dict(l=60, r=20, t=20, b=45),
                height=420,
                dragmode=False,
                hovermode="x unified"
            )

            suruklenebilir_lejantli_plotly(aylik_fig, height=440)

            if secilen_yil == "Tüm Yıllar":
                st.caption(
                    f"{_ozet_gorunum} kullanılıyor. Her ay, seçilen tarih aralığındaki "
                    "bütün yılların aynı takvim ayı kayıtlarından hesaplanır."
                )
            else:
                st.caption(
                    f"{_ozet_gorunum} kullanılıyor. Yalnızca {secilen_yil} yılı hesaplanıyor."
                )

        # --------------------------------------------------------
        # Mean diurnal profile
        # --------------------------------------------------------

        with sag_alt:
            baslik_col, utc_col = st.columns([3, 1])

            with baslik_col:
                st.subheader("Mean Diurnal Profile")

            with utc_col:
                logger_utc_farki = st.selectbox(
                    "Logger UTC farkı",
                    options=[0, 1, 2, 3, 4],
                    index=3,
                    format_func=lambda x: f"UTC+{x}",
                    key="logger_utc_farki"
                )

            saatlik_veri = ana_sayfa_verisi[
                ["TIMESTAMP"] + RUZGAR_KOLONLARI
            ].copy()
            saatlik_veri = saatlik_veri.replace([np.inf, -np.inf], np.nan)

            for kolon in RUZGAR_KOLONLARI:
                saatlik_veri.loc[
                    (saatlik_veri[kolon] < 0)
                    | (saatlik_veri[kolon] > 45),
                    kolon
                ] = np.nan

            # Logger zamanını UTC'ye çevir.
            utc_zamani = (
                saatlik_veri["TIMESTAMP"]
                - pd.to_timedelta(logger_utc_farki, unit="h")
            )
            saatlik_veri["Saat"] = utc_zamani.dt.hour

            gunluk_profil = (
                saatlik_veri
                .groupby("Saat", observed=False)[RUZGAR_KOLONLARI]
                .mean()
                .reindex(range(24))
                .rename(columns=AKTIF_GORUNUR_ADLAR)
                .reset_index()
            )

            gunluk_uzun = gunluk_profil.melt(
                id_vars="Saat",
                value_vars=[AKTIF_GORUNUR_ADLAR[k] for k in RUZGAR_KOLONLARI],
                var_name="Sensör",
                value_name="Rüzgar Hızı"
            )

            gunluk_fig = px.line(
                gunluk_uzun,
                x="Saat",
                y="Rüzgar Hızı",
                color="Sensör",
                color_discrete_map={
                    AKTIF_GORUNUR_ADLAR["WS1_Avg"]: "#0875D1",
                    AKTIF_GORUNUR_ADLAR["WS2_Avg"]: "#69B9FF",
                    AKTIF_GORUNUR_ADLAR["WS3_Avg"]: "#FF2B2B",
                    AKTIF_GORUNUR_ADLAR["WS4_Avg"]: "#FF9C9C",
                },
                markers=True,
                category_orders={
                    "Sensör": [AKTIF_GORUNUR_ADLAR[k] for k in RUZGAR_KOLONLARI]
                },
                labels={
                    "Saat": "Hour of Day (UTC)",
                    "Rüzgar Hızı": "Mean Wind Speed (m/s)"
                }
            )

            gunluk_fig.update_traces(
                marker=dict(symbol="circle", size=6),
                line=dict(width=2.2),
                connectgaps=False,
                hovertemplate=(
                    "%{fullData.name}<br>"
                    "%{x}:00 UTC — %{y:.3f} m/s<extra></extra>"
                )
            )

            gunluk_degerler = gunluk_uzun["Rüzgar Hızı"].dropna()
            if gunluk_degerler.empty:
                y_min, y_max = 0.0, 8.0
            else:
                alt = float(gunluk_degerler.min())
                ust = float(gunluk_degerler.max())
                bosluk = max((ust - alt) * 0.20, 0.30)
                y_min = max(0.0, np.floor((alt - bosluk) * 2) / 2)
                y_max = np.ceil((ust + bosluk) * 2) / 2
                if y_max <= y_min:
                    y_max = y_min + 1.0

            gunluk_fig.update_layout(
                xaxis=dict(
                    title="Hour of Day (UTC)",
                    range=[0, 23],
                    tickmode="array",
                    tickvals=[0, 3, 6, 9, 12, 15, 18, 21, 23],
                    ticktext=["0", "3", "6", "9", "12", "15", "18", "21", "24"],
                    fixedrange=True,
                    showgrid=True,
                    zeroline=False
                ),
                yaxis=dict(
                    title="Mean Wind Speed (m/s)",
                    range=[y_min, y_max],
                    dtick=0.5,
                    fixedrange=True,
                    showgrid=True,
                    zeroline=False
                ),
                legend=dict(
                    x=0.02,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="rgba(255,255,255,0.90)",
                    bordercolor="black",
                    borderwidth=1
                ),
                margin=dict(l=60, r=20, t=20, b=50),
                height=420,
                dragmode=False,
                hovermode="x unified"
            )

            suruklenebilir_lejantli_plotly(gunluk_fig, height=440)

            st.caption(
                f"Logger zaman damgaları UTC+{logger_utc_farki} kabul edilip "
                "UTC saatlerine dönüştürülmüştür."
            )

        # --------------------------------------------------------
        # Ölçüm direği koordinatları (isteğe bağlı)
        # --------------------------------------------------------
        with st.expander("Ölçüm Direği Koordinatları (rüzgar haritası için)", expanded=False):
            bolum_basligi("Ölçüm Direği Koordinatları", "Rüzgar haritasında kullanılacak direkleri seçin ve konum bilgilerini doğrulayın.")
            st.info(
                "Rüzgar haritasında kullanmak istediğiniz ölçüm direklerini seçin ve "
                "koordinatlarını doğrulayın."
            )

            for sira, dosya_adi in enumerate(tum_veri_setleri.keys(), start=1):
                if dosya_adi != aktif_dosya_adi:
                    continue
                with st.expander(dosya_adi, expanded=True):
                    konum_kullan = st.checkbox(
                        "Bu direği rüzgar haritasında kullan",
                        key=f"direk_kullan_{sira}"
                    )

                    koordinat_col1, koordinat_col2 = st.columns(2)
                    with koordinat_col1:
                        lat = st.number_input(
                            "Enlem",
                            min_value=-90.0,
                            max_value=90.0,
                            step=0.000001,
                            format="%.6f",
                            key=f"direk_lat_{sira}",
                            disabled=not konum_kullan
                        )
                    with koordinat_col2:
                        lon = st.number_input(
                            "Boylam",
                            min_value=-180.0,
                            max_value=180.0,
                            step=0.000001,
                            format="%.6f",
                            key=f"direk_lon_{sira}",
                            disabled=not konum_kullan
                        )

                    if konum_kullan and lat == 0.0 and lon == 0.0:
                        st.warning("Rüzgar direğinin konumunu girin.")

            # Widget değişikliklerinden sonra koordinat sözlüğünü güncelle.
            direk_koordinatlari = {}
            for sira, dosya_adi in enumerate(tum_veri_setleri.keys(), start=1):
                konum_kullan = bool(st.session_state.get(f"direk_kullan_{sira}", False))
                lat = float(st.session_state.get(f"direk_lat_{sira}", 0.0))
                lon = float(st.session_state.get(f"direk_lon_{sira}", 0.0))
                if konum_kullan and not (lat == 0.0 and lon == 0.0):
                    direk_koordinatlari[dosya_adi] = {"lat": lat, "lon": lon}




# ============================================================
# VERİ İNCELEME — HAM VE GERÇEK TEMİZ ÖLÇÜMLER
# ============================================================
elif sayfa == "Veri İnceleme":
    _islem_gorunum = st.radio("Veri görünümü", ["Ham Veri", "Temizlenmiş Veri"],
                              horizontal=True, key="inceleme_gorunumu_v11119")
    _islem_veri = (filtreli_veri.copy() if _islem_gorunum == "Ham Veri"
                   else olcum_kalite_verisi(filtreli_veri, aktif_dosya_adi))
    st.caption("Temizlenmiş görünümde fiziksel sınır dışı, otomatik kalite işaretli ve manuel işaretli ölçümler boş bırakılır. Tahmini kayıtlar gerçek temiz ölçüm sayılmaz.")
    _islem_cols = [c for c in RUZGAR_KOLONLARI if c in _islem_veri.columns]
    _i1, _i2, _i3 = st.columns(3)
    _i1.metric("Kayıt", f"{len(_islem_veri):,}")
    _i2.metric("Hız sensörü", len(_islem_cols))
    _i3.metric("Görünüm", _islem_gorunum)
    with st.expander("Zaman serisi grafiği", expanded=False):
        st.line_chart(_islem_veri.set_index("TIMESTAMP")[_islem_cols].resample("1h").mean()
                      .rename(columns=AKTIF_GORUNUR_ADLAR), use_container_width=True)
    _islem_tablo = _islem_veri[["TIMESTAMP"] + _islem_cols].rename(columns=AKTIF_GORUNUR_ADLAR)
    st.dataframe(_islem_tablo, hide_index=True, use_container_width=True, height=380)
    st.download_button("Gösterilen veriyi CSV indir", _islem_tablo.to_csv(index=False).encode("utf-8-sig"),
                       file_name="ruzgar_olcumleri.csv", mime="text/csv")
    st.button("Sorunlu ölçümleri işaretle →", on_click=navigasyona_git, args=("Rüzgar Kaynağı Özeti",))
    with st.expander("Gelişmiş: mevcut otomatik filtreleme ve tahminle tamamlama", expanded=False):
        st.caption("Eski yöntem korunmuştur. Sabit ölçüm ve sensör farkı şüpheleri otomatik dışlanır; uygun sensörlerden α=0,14 ile eksikler tamamlanır. Bu çıktı gerçek temiz ölçüm katmanından farklıdır ve eşikleri henüz doğrulanmamıştır. Manuel kalite işaretlerini kullanmaz.")
        if st.checkbox("Deneysel çıktıyı göster", key="ileri_islem_v11119"):
            _ileri_veri, _ileri_kalite = hizli_temizle(filtreli_veri, AKTIF_SENSOR_YUKSEKLIKLERI)
            _ileri_tablo = _ileri_veri[["TIMESTAMP"] + _islem_cols].rename(columns=AKTIF_GORUNUR_ADLAR)
            st.dataframe(_ileri_tablo, hide_index=True, use_container_width=True, height=300)
            st.dataframe(_ileri_kalite.apply(pd.Series.value_counts).fillna(0), use_container_width=True)
            st.download_button("Tahmin içeren veriyi CSV indir", _ileri_tablo.to_csv(index=False).encode("utf-8-sig"),
                               file_name="otomatik_filtreli_tahmin_iceren_veri.csv", mime="text/csv")

# ============================================================
# YÜKSEK ÇÖZÜNÜRLÜKLÜ TOPOĞRAFYA MODÜLÜ
# ============================================================
elif sayfa == "Topografya Modülü":
    bolum_basligi(
        "Yüksek Çözünürlüklü Topografya ve Halihazır Harita",
        "1/1000 ve 1/5000 halihazır haritalardan kot verisini okuyun, çalışma tamponunu tanımlayın ve DEM önizlemesini oluşturun. Mevcut analiz ve micrositing kodları değiştirilmeden ayrı bir modül olarak çalışır."
    )

    st.info(
        "En güvenilir girişler GeoTIFF DEM, LandXML, DXF içindeki 3B polylineler veya X-Y-Z kot noktalarıdır. "
        "DWG/NCZ dosyaları lisanslı dönüştürücü gerektirdiği için bu ilk sürümde yüklenip kaydedilir; hesap için DXF, LandXML, GeoTIFF ya da CSV/XYZ çıktısı kullanılmalıdır."
    )

    ayar1, ayar2, ayar3, ayar4 = st.columns(4)
    with ayar1:
        _topo_scale = st.selectbox("Halihazır harita ölçeği", ["1/1000", "1/5000", "Özel"], index=1, key="topo_scale_v113")
    with ayar2:
        _vars_grid = 2.0 if _topo_scale == "1/1000" else 5.0
        _topo_grid = st.number_input("DEM grid çözünürlüğü (m)", min_value=0.5, max_value=100.0, value=float(_vars_grid), step=0.5, key="topo_grid_v113")
    with ayar3:
        _topo_buffer = st.number_input("Santral dışı çalışma tamponu (km)", min_value=0.0, max_value=50.0, value=5.0, step=0.5, key="topo_buffer_v113")
    with ayar4:
        _topo_crs = st.text_input("Koordinat sistemi / EPSG", value=app_state.get("highres_topography_crs", ""), placeholder="Örn. EPSG:5254 veya ITRF96 3°", key="topo_crs_v113")

    _topo_files = st.file_uploader(
        "Halihazır harita / arazi modeli yükle",
        type=["tif", "tiff", "csv", "xyz", "txt", "dxf", "dwg", "ncz", "xml"],
        accept_multiple_files=True,
        key="highres_topography_upload_v113",
        help="Birden fazla GeoTIFF, CSV/XYZ, LandXML ve Z değerli DXF yüklenebilir.",
    )
    _topo_file = _topo_files[0] if _topo_files else None

    if _topo_file is None:
        st.markdown(
            """
            <div class="empty-state">
              <h3>Halihazır haritayı yükleyin</h3>
              <p>Kot noktaları, eşyükselti/3B polyline veya hazır DEM yüklendiğinde arazi kapsamı ve DEM önizlemesi burada gösterilir.</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.stop()

    _uzanti = Path(_topo_file.name).suffix.lower()
    _bytes = _topo_file.getvalue()
    _summary = {"dosya": _topo_file.name, "boyut_mb": len(_bytes)/(1024*1024), "olcek": _topo_scale,
                "grid_m": float(_topo_grid), "tampon_km": float(_topo_buffer), "crs_kullanici": _topo_crs}
    _points = None
    _preview = None
    _katmanlar = None
    try:
        if _uzanti in {".tif", ".tiff"}:
            _geo = _topografya_geotiff_ozeti(_bytes)
            _summary.update(_geo)
            _preview = _geo.pop("preview", None)
        elif _uzanti in {".csv", ".xyz", ".txt"}:
            _points = _topografya_csv_xyz_oku(_bytes, _topo_file.name)
            _summary.update({"tip": "X-Y-Z kot noktaları", "nokta_sayisi": int(len(_points)),
                             "min_kot": float(_points.Z.min()), "max_kot": float(_points.Z.max()),
                             "x_aralik": [float(_points.X.min()), float(_points.X.max())],
                             "y_aralik": [float(_points.Y.min()), float(_points.Y.max())]})
        elif _uzanti == ".xml":
            _points = _topografya_landxml_oku(_bytes)
            _summary.update({"tip": "LandXML kot/TIN noktaları", "nokta_sayisi": int(len(_points)),
                             "min_kot": float(_points.Z.min()), "max_kot": float(_points.Z.max()),
                             "x_aralik": [float(_points.X.min()), float(_points.X.max())],
                             "y_aralik": [float(_points.Y.min()), float(_points.Y.max())]})
        elif _uzanti == ".dxf":
            _points, _katmanlar = _topografya_dxf_oku(_bytes)
            _summary.update({"tip": "DXF 3B kot verisi", "nokta_sayisi": int(len(_points)),
                             "min_kot": float(_points.Z.min()), "max_kot": float(_points.Z.max()),
                             "x_aralik": [float(_points.X.min()), float(_points.X.max())],
                             "y_aralik": [float(_points.Y.min()), float(_points.Y.max())],
                             "katman_sayisi": len(_katmanlar)})
        else:
            _summary.update({"tip": f"{_uzanti[1:].upper()} kaynak dosyası", "durum": "Dönüşüm gerekli"})
            app_state["highres_topography_file"] = dosyayi_kaydet(_topo_file)
            app_state["highres_topography_summary"] = _summary
            st.warning("Dosya kaydedildi; sayısal arazi hesabı için Netcad/AutoCAD'den Z değerli DXF, LandXML, GeoTIFF veya X-Y-Z CSV dışa aktarın.")
            st.json(_summary)
            st.stop()
    except Exception as hata:
        st.error(f"Topografya dosyası işlenemedi: {hata}")
        st.stop()

    app_state["highres_topography_file"] = dosyayi_kaydet(_topo_file)
    app_state["highres_topography_summary"] = {k:v for k,v in _summary.items() if k != "preview"}
    app_state["highres_topography_crs"] = _topo_crs
    app_state["highres_topography_scale"] = _topo_scale
    app_state["highres_topography_grid_m"] = float(_topo_grid)
    app_state["highres_topography_buffer_km"] = float(_topo_buffer)

    st.success("Halihazır harita başarıyla okundu. Mevcut uygulama modüllerine dokunulmadı; arazi verisi ayrı oturum kaydı olarak hazırlandı.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Kaynak", _summary.get("tip", "—"))
    m2.metric("Kot min–maks", f"{_summary.get('min_kot', float('nan')):.1f} – {_summary.get('max_kot', float('nan')):.1f} m" if "min_kot" in _summary else "—")
    m3.metric("Grid", f"{float(_topo_grid):g} m")
    m4.metric("Çalışma tamponu", f"{float(_topo_buffer):g} km")

    if _katmanlar:
        with st.expander("DXF katman özeti"):
            guvenli_dataframe(pd.DataFrame([{"Katman": k, "Eleman": v} for k,v in sorted(_katmanlar.items())]), use_container_width=True, hide_index=True)

    if _points is not None:
        st.markdown("### Kot noktaları ve DEM önizlemesi")
        sol, sag = st.columns([0.42, 0.58], gap="large")
        with sol:
            guvenli_dataframe(_points.head(1000), use_container_width=True, height=430)
            st.caption(f"Toplam {_points.shape[0]:,} geçerli kot noktası. Önizleme tablosu ilk 1.000 kaydı gösterir.")
        with sag:
            with st.spinner("Kot noktalarından ön DEM oluşturuluyor..."):
                gx, gy, dem = _topografya_nokta_dem_uret(_points, grid_m=float(_topo_grid))
            fig_dem = go.Figure(go.Heatmap(x=gx, y=gy, z=dem, colorscale="Earth", colorbar=dict(title="Kot (m)")))
            fig_dem.update_layout(title="Yüksek Çözünürlüklü DEM Önizlemesi", xaxis_title="X / Easting", yaxis_title="Y / Northing", height=520, margin=dict(l=40,r=20,t=55,b=40))
            st.plotly_chart(fig_dem, use_container_width=True, config={"displaylogo": False})
            app_state["highres_topography_points"] = _points.to_dict("records") if len(_points) <= 15000 else None
    elif _preview is not None:
        st.markdown("### GeoTIFF DEM önizlemesi")
        fig_dem = go.Figure(go.Heatmap(z=_preview, colorscale="Earth", colorbar=dict(title="Kot (m)")))
        fig_dem.update_layout(height=560, margin=dict(l=30,r=20,t=35,b=30), xaxis_title="Raster sütunu", yaxis_title="Raster satırı")
        st.plotly_chart(fig_dem, use_container_width=True, config={"displaylogo": False})

    st.markdown("### Rüzgâr haritası entegrasyon durumu")
    st.success(
        "Yüksek çözünürlüklü arazi veri seti hazır. Sonraki hesapta bu DEM, mevcut SRTM90m katmanının yerine seçilebilir kaynak olarak kullanılabilecek şekilde oturumda saklanıyor. "
        "Santral dışı çalışma alanı için seçilen tampon değeri de kaydedildi."
    )
    st.caption("Not: Bu modül arazi verisini güvenli biçimde hazırlar. Bankable rüzgâr akış sonucu için WAsP/WindPRO/CFD doğrulaması ayrıca gereklidir.")


# ============================================================
# ÜRETİM HESAPLAMA
# ============================================================
# ============================================================
# ÜRETİM HESAPLAMA
# ============================================================

elif sayfa == "Üretim Hesaplama":

    bolum_basligi("Rüzgâr Kaynağı, Türbin Yerleşimi ve Enerji Üretimi", "Global Wind Atlas rüzgâr alanı + ölçüm direği kalibrasyonu + türbin yerleşimi + AEP.")
    st.caption(
        "Global Wind Atlas tabanlı rüzgâr haritası, türbin yerleşimi ve enerji üretimi tek sayfada birlikte gösterilir."
    )

    # Micrositing başlamadan önce sade halihazır harita yükleme adımı.
    # Teknik CRS/ölçek/grid/ODA alanları müşteriye gösterilmez; mevcut varsayılanlar arka planda korunur.
    if not app_state.get("micrositing_topography_ready", False):
        bolum_basligi(
            "Halihazır Harita (İsteğe Bağlı)",
            "Varsa halihazır haritanızı yükleyin; yoksa bu adımı atlayıp doğrudan rüzgâr haritasına geçebilirsiniz."
        )

        _ms_topo_crs = str(app_state.get("highres_topography_crs", "") or "")
        _ms_topo_scale = str(app_state.get("highres_topography_scale", "1/5000") or "1/5000")
        _ms_topo_grid = float(app_state.get("highres_topography_grid_m", 5.0) or 5.0)
        _oda_path = str(app_state.get("oda_converter_path", "") or "")

        _ms_topo_files = st.file_uploader(
            "Halihazır harita yükle",
            type=["tif", "tiff", "csv", "xyz", "txt", "dxf", "xml", "landxml", "dwg", "ncz"],
            accept_multiple_files=True,
            key="micrositing_multi_topography_upload_v1184",
            help="DWG, DXF, GeoTIFF, LandXML ve X-Y-Z tabanlı halihazır haritalar desteklenir.",
        )

        if _ms_topo_files:
            if st.button("Rüzgâr haritasına geç →", type="primary", use_container_width=True):
                _kullanilabilir = []
                _hatalar = []
                with st.spinner("Halihazır harita hazırlanıyor..."):
                    for _f in _ms_topo_files:
                        try:
                            _kayit = _topografya_yuklemesini_hesap_kaydina_cevir(_f, _oda_path)
                            _kullanilabilir.append(_kayit)
                        except Exception as _hata:
                            _hatalar.append(f"{_f.name}: {_hata}")

                if _hatalar:
                    for _hata in _hatalar:
                        st.error(_hata)

                if _kullanilabilir:
                    app_state["highres_topography_files"] = _kullanilabilir
                    app_state["highres_topography_file"] = _kullanilabilir[0]
                    app_state["highres_topography_crs"] = _ms_topo_crs
                    app_state["highres_topography_scale"] = _ms_topo_scale
                    app_state["highres_topography_grid_m"] = float(_ms_topo_grid)
                    app_state["micrositing_topography_ready"] = True
                    kalici_durumu_kaydet(app_state)
                    st.rerun()
                elif not _hatalar:
                    st.error("Halihazır harita işlenemedi.")
        else:
            st.info(
                "Halihazır harita isteğe bağlıdır. Yüklemeden devam ederseniz "
                "arazi kotları mevcut çevrimiçi/varsayılan topoğrafya kaynağından tamamlanır."
            )
            if st.button(
                "Halihazır harita yüklemeden devam et →",
                type="primary",
                use_container_width=True,
                key="micrositing_topo_atla_v1100",
            ):
                app_state["highres_topography_files"] = []
                app_state["highres_topography_file"] = None
                app_state["micrositing_topography_ready"] = True
                kalici_durumu_kaydet(app_state)
                st.rerun()
        st.stop()

    _topo_sayisi = len(app_state.get("highres_topography_files", [])) or (1 if app_state.get("highres_topography_file") else 0)
    _topo_bar1, _topo_bar2 = st.columns([4, 1])
    with _topo_bar1:
        if _topo_sayisi:
            st.success(f"{_topo_sayisi} halihazır topoğrafya kaynağı Micrositing hesabına bağlı.")
        else:
            st.info("Halihazır harita kullanılmıyor · Micrositing varsayılan topoğrafya kaynağıyla devam ediyor.")
    with _topo_bar2:
        if st.button(
            "Halihazır ekle / değiştir",
            use_container_width=True,
            key="micrositing_topo_degistir_v1100",
        ):
            app_state["micrositing_topography_ready"] = False
            st.rerun()

    # Micrositing akışı tekrar üç ayrı alt sekmede gösterilir.
    sekme_saha, sekme_turbin, sekme_sonuc = st.tabs([
        "1 · Rüzgâr Haritası",
        "2 · Türbin Yerleşimi",
        "3 · Enerji Üretimi",
    ])

    st.success("Enerji girdisi: fiziksel, otomatik ve manuel kalite kontrollerinden kalan gerçek ölçümler. Eksik kayıtlar doldurulmaz. Sonuç güç eğrisiyle hesaplanan tahmindir; ölçülmüş elektrik üretimi değildir.")
    temiz_veri = olcum_kalite_verisi(filtreli_veri, aktif_dosya_adi)

    # --------------------------------------------------------
    # 1) SAHA GİRDİLERİ + SAHA HARİTASI İÇİN YER AYIR
    # --------------------------------------------------------
    with sekme_saha:
        st.subheader("1 · Rüzgâr Haritası")
        saha_sol, saha_sag = st.columns([0.34, 0.66], gap="large")

        with saha_sol:
            _yuklenen_santral_siniri = st.file_uploader(
                "Santral sınırı (KML / KMZ)",
                type=["kml", "kmz"],
                key=f"santral_boundary_uploader_{app_state['boundary_uploader_nonce']}",
                help="Google Earth üzerinde çizilmiş santral sınırını yükleyin."
            )
            if tek_yukleme_degisti(_yuklenen_santral_siniri, app_state.get("santral_boundary")):
                app_state["santral_boundary"] = dosyayi_kaydet(_yuklenen_santral_siniri)
            santral_siniri = kayitli_dosyayi_olustur(app_state.get("santral_boundary"))

            if santral_siniri is not None:
                st.success(f"Santral sınırı hazır: {santral_siniri.name}")
                if st.button("Santral sınırını değiştir", key="santral_boundary_temizle"):
                    app_state["santral_boundary"] = None
                    app_state["wind_map_center"] = None
                    app_state["wind_grid"] = None
                    app_state["turbine_layout"] = None
                    app_state["wake_result"] = None
                    app_state["production_result"] = None
                    app_state["boundary_uploader_nonce"] += 1
                    st.rerun()

            # Kullanıcının rüzgâr haritası çalışma alanı boyutunu ayarlamasına izin ver.
            # Bu yalnızca haritanın kare çalışma alanını değiştirir; GWA, kalibrasyon,
            # türbin yerleşimi ve enerji hesabı mantığına dokunmaz.
            _onceki_harita_alani = float(app_state.get("wind_map_area_km", 10.0) or 10.0)
            _harita_alani_km = st.number_input(
                "Rüzgâr haritası alanı (km)",
                min_value=1.0,
                max_value=50.0,
                value=_onceki_harita_alani,
                step=1.0,
                format="%.1f",
                help="Santral sınırının merkezi etrafında oluşturulacak kare rüzgâr haritasının kenar uzunluğu."
            )
            if float(_harita_alani_km) != _onceki_harita_alani:
                app_state["wind_map_area_km"] = float(_harita_alani_km)
                app_state["wind_grid"] = None
                app_state["turbine_layout"] = None
                app_state["wake_result"] = None
                app_state["production_result"] = None
            else:
                app_state["wind_map_area_km"] = float(_harita_alani_km)

            st.caption(
                f"Çalışma alanı: {float(app_state['wind_map_area_km']):.1f} km × "
                f"{float(app_state['wind_map_area_km']):.1f} km"
            )

            _onceki_yogunluk = int(app_state.get("wind_map_grid_density", 60) or 60)
            _nokta_yogunlugu = st.number_input(
                "Rüzgâr haritası nokta yoğunluğu",
                min_value=24,
                max_value=120,
                value=_onceki_yogunluk,
                step=6,
                help="Haritanın her eksenindeki örnekleme noktası sayısı. Yüksek değer daha ayrıntılı, ancak daha yavaş hesaplama yapar."
            )
            if int(_nokta_yogunlugu) != _onceki_yogunluk:
                app_state["wind_map_grid_density"] = int(_nokta_yogunlugu)
                app_state["wind_grid"] = None
                app_state["turbine_layout"] = None
                app_state["wake_result"] = None
                app_state["production_result"] = None
            else:
                app_state["wind_map_grid_density"] = int(_nokta_yogunlugu)

            st.caption(
                f"Grid: {int(app_state['wind_map_grid_density'])} × "
                f"{int(app_state['wind_map_grid_density'])} nokta"
            )

            st.success(
                "Rüzgâr haritası yöntemi: GWA + Ölçüm Kalibrasyonu. "
                "Global Wind Atlas saha üzerindeki mekânsal dağılımı sağlar; "
                "LoggerNet ölçüm direkleri bu alanı gerçek saha ölçümleriyle kalibre eder."
            )

            # Müşteri ekranında teknik GWA/konum/grid kontrolleri gösterilmez.
            # Mevcut hesap varsayımları ve daha önce tanımlanmış ölçüm direği konumları arka planda kullanılır.
            app_state["wind_map_engine"] = "Global Wind Atlas (GWA)"
            app_state["wind_map_preserve_mean"] = True
            app_state["gwa_auto_download"] = True
            app_state["gwa_calibrate_to_masts"] = True
            app_state["gwa_wind_tif"] = None
            app_state["gwa_api_url"] = ""
            _gwa_yukseklikler = [10, 50, 100, 150, 200]
            _hub = float(app_state.get("hub_height", 100.0) or 100.0)
            app_state["gwa_height_m"] = int(min(_gwa_yukseklikler, key=lambda h: abs(float(h) - _hub)))

            yasak_alan_dosyasi = kayitli_dosyayi_olustur(app_state.get("restricted_areas"))

            secili_veri_setleri = [aktif_dosya_adi]
            app_state["micrositing_selected_wind_data"] = list(secili_veri_setleri)

            secili_tum_veriler = {ad: tum_veri_setleri[ad] for ad in secili_veri_setleri}
            secili_filtreli_veriler = {}
            for _ad, _veri in secili_tum_veriler.items():
                _filtreli = _veri[
                    (_veri["TIMESTAMP"].dt.date >= baslangic_tarihi)
                    & (_veri["TIMESTAMP"].dt.date <= bitis_tarihi)
                ].copy()
                if not _filtreli.empty:
                    secili_filtreli_veriler[_ad] = _filtreli

            gecerli_direk_sayisi = sum(1 for ad in secili_veri_setleri if ad in direk_koordinatlari)
            zorunlu_hazir = bool(santral_siniri) and gecerli_direk_sayisi >= 1
            if not santral_siniri:
                st.info("Rüzgâr haritasını oluşturmak için santral sınırını yükleyin.")
            elif gecerli_direk_sayisi < 1:
                st.warning("Seçili ölçüm direğinin kurulum raporunda geçerli koordinat bulunamadı.")

            if zorunlu_hazir:
                kalite_seviyesi = "Analiz hazır"
                otomatik_yontem = "Otomatik saha analizi"
                kalite_notu = "Saha ve ölçüm verileri analiz için hazır."
            else:
                kalite_seviyesi = "Girdi bekleniyor"
                otomatik_yontem = "Henüz belirlenemedi"
                kalite_notu = "Santral sınırı ve ölçüm direği konumu bekleniyor."

        with saha_sag:
            saha_harita_alani = st.container()

    # --------------------------------------------------------
    # 2) TÜRBİN AYARLARI + YERLEŞİM HARİTASI İÇİN YER AYIR
    # --------------------------------------------------------
    with sekme_turbin:
        st.subheader("Türbin ayarları ve yerleşim")
        turbin_sol, turbin_sag = st.columns([0.34, 0.66], gap="large")

        with turbin_sol:
            _uretici_secenekleri = list(TURBIN_KUTUPHANESI.keys())
            _kayitli_uretici = app_state.get("turbine_manufacturer", _uretici_secenekleri[0])
            _uretici_index = _uretici_secenekleri.index(_kayitli_uretici) if _kayitli_uretici in _uretici_secenekleri else 0
            uretici = st.selectbox(
                "Türbin üreticisi",
                options=_uretici_secenekleri,
                index=_uretici_index,
                key="uretim_uretici_widget"
            )
            app_state["turbine_manufacturer"] = uretici
            model_secenekleri = list(TURBIN_KUTUPHANESI[uretici].keys())
            _kayitli_model = app_state.get("turbine_model")
            _model_index = model_secenekleri.index(_kayitli_model) if _kayitli_model in model_secenekleri else 0
            model = st.selectbox(
                "Türbin modeli",
                options=model_secenekleri,
                index=_model_index,
                key=f"uretim_model_widget_{uretici}"
            )
            app_state["turbine_model"] = model
            model_bilgisi = TURBIN_KUTUPHANESI[uretici][model]

            hub_yuksekligi = st.number_input(
                "Hub yüksekliği (m)",
                min_value=1.0,
                max_value=300.0,
                value=float(app_state.get("hub_height") or model_bilgisi["hub_yukseklikleri_m"][0]),
                step=1.0,
                format="%.1f",
                key=f"uretim_hub_widget_{uretici}_{model}"
            )
            app_state["hub_height"] = float(hub_yuksekligi)
            turbin_sayisi = st.number_input(
                "Türbin sayısı",
                min_value=1,
                max_value=100,
                value=int(app_state.get("turbine_count", 10)),
                step=1,
                key="uretim_turbin_sayisi_widget"
            )
            app_state["turbine_count"] = int(turbin_sayisi)

            if app_state.get("turbine_placement_mode") in {"Manuel koordinat girişi", "Haritadan manuel yerleşim"}:
                app_state["turbine_placement_mode"] = "Manuel / Excel yerleşimi"

            yerlesim_modu = st.radio(
                "Türbin yerleşim yöntemi",
                options=["Otomatik yerleşim", "Manuel / Excel yerleşimi"],
                index=0 if app_state.get("turbine_placement_mode", "Otomatik yerleşim") == "Otomatik yerleşim" else 1,
                horizontal=True,
                key="turbin_yerlesim_modu_v1191",
            )
            app_state["turbine_placement_mode"] = yerlesim_modu

            if yerlesim_modu == "Manuel / Excel yerleşimi":
                st.info(
                    "Türbinleri iki şekilde ekleyebilirsiniz: haritaya tıklayarak veya "
                    "Enlem/Boylam sütunları bulunan Excel/CSV dosyasını yükleyerek."
                )

                _koordinat_sistemleri = [
                    "WGS84 / Enlem-Boylam",
                    "ITRF96 / TM3",
                    "ED50 / UTM 6°",
                    "Özel EPSG",
                ]
                _kayitli_ks = app_state.get("manual_turbine_coord_system", "WGS84 / Enlem-Boylam")
                _ks_index = _koordinat_sistemleri.index(_kayitli_ks) if _kayitli_ks in _koordinat_sistemleri else 0
                _koordinat_sistemi = st.selectbox(
                    "Excel koordinat sistemi",
                    options=_koordinat_sistemleri,
                    index=_ks_index,
                    key="turbin_excel_koordinat_sistemi_v1192",
                )
                app_state["manual_turbine_coord_system"] = _koordinat_sistemi

                _iller = list(TURKIYE_IL_BOYLAMLARI.keys())
                _kayitli_il = str(app_state.get("manual_turbine_province", "Ankara") or "Ankara")
                if _kayitli_il not in _iller:
                    _kayitli_il = "Ankara"
                _il = st.selectbox(
                    "Proje ili / bölgesi",
                    options=_iller,
                    index=_iller.index(_kayitli_il),
                    key="turbin_excel_il_v1100",
                )
                app_state["manual_turbine_province"] = _il

                _ed50_zone, _itrf_cm = _ilden_utm_zonu_ve_tm3_meridyeni(_il)
                app_state["manual_turbine_ed50_zone"] = int(_ed50_zone)
                app_state["manual_turbine_itrf_cm"] = int(_itrf_cm)
                _custom_epsg = int(app_state.get("manual_turbine_custom_epsg", 4326) or 4326)

                if _koordinat_sistemi == "ITRF96 / TM3":
                    st.caption(
                        f"{_il} için ITRF96 / TM3 merkezi meridyeni otomatik seçildi: "
                        f"{_itrf_cm}° · Excel sütunları X (Easting) / Y (Northing)."
                    )
                elif _koordinat_sistemi == "ED50 / UTM 6°":
                    st.caption(
                        f"{_il} için ED50 / UTM zonu otomatik seçildi: "
                        f"{_ed50_zone}N · Excel sütunları X (Easting) / Y (Northing)."
                    )
                elif _koordinat_sistemi == "Özel EPSG":
                    _custom_epsg = int(st.number_input(
                        "Kaynak EPSG kodu",
                        min_value=1,
                        max_value=999999,
                        value=_custom_epsg,
                        step=1,
                        key="turbin_excel_custom_epsg_v1100",
                    ))
                    app_state["manual_turbine_custom_epsg"] = _custom_epsg
                else:
                    st.caption("Excel sütunları: Enlem ve Boylam (ondalık derece).")

                _turbin_excel = st.file_uploader(
                    "Türbin koordinatları (Excel / CSV)",
                    type=["xlsx", "xls", "csv"],
                    key="turbin_excel_yukle_v1191",
                    help="WGS84 seçiliyse Enlem/Boylam; ITRF96, ED50 veya özel EPSG seçiliyse X/Y (Easting/Northing) sütunları kullanılır. Türbin/Name/ID sütunu isteğe bağlıdır."
                )

                if _turbin_excel is not None:
                    _excel_imza = (
                        f"{_turbin_excel.name}:{getattr(_turbin_excel, 'size', 0)}:"
                        f"{_koordinat_sistemi}:{_ed50_zone}:{_itrf_cm}:{_custom_epsg}"
                    )
                    _onceki_excel_imza = str(app_state.get("manual_turbine_excel_name", "") or "")
                    if _excel_imza != _onceki_excel_imza:
                        try:
                            _excel_noktalar, _excel_uyarilar, _excel_ozet = turbin_excel_noktalarini_oku(
                                _turbin_excel,
                                koordinat_sistemi=_koordinat_sistemi,
                                ed50_zone=_ed50_zone,
                                itrf_cm=_itrf_cm,
                                custom_epsg=_custom_epsg,
                            )

                            # ED50/UTM'de yanlış zon seçimi noktaları yüzlerce km kaydırabilir.
                            # Santral sınırı varsa 35N-38N zonlarını otomatik deneyip,
                            # sınır içinde en çok türbin veren zonu seç.
                            _otomatik_ed50_zone = None
                            _excel_santral_poligonu = None
                            try:
                                _kayitli_sinir = kayitli_dosyayi_olustur(app_state.get("santral_boundary"))
                                if _kayitli_sinir is not None:
                                    _excel_santral_poligonu = kml_kmz_sinirlarini_oku(_kayitli_sinir)
                            except Exception:
                                _excel_santral_poligonu = None

                            if _koordinat_sistemi == "ED50 / UTM 6°" and _excel_santral_poligonu:
                                _zon_sonuclari = []
                                for _zon in (35, 36, 37, 38):
                                    try:
                                        _zon_noktalar, _zon_uyarilar, _zon_ozet = turbin_excel_noktalarini_oku(
                                            _turbin_excel,
                                            koordinat_sistemi=_koordinat_sistemi,
                                            ed50_zone=_zon,
                                            itrf_cm=_itrf_cm,
                                            custom_epsg=_custom_epsg,
                                        )
                                        _icerde = sum(
                                            1 for _n in _zon_noktalar
                                            if nokta_poligon_icinde(
                                                float(_n["lon"]),
                                                float(_n["lat"]),
                                                _excel_santral_poligonu,
                                            )
                                        )
                                        _zon_sonuclari.append((_icerde, _zon, _zon_noktalar, _zon_uyarilar, _zon_ozet))
                                    except Exception:
                                        pass

                                if _zon_sonuclari:
                                    _zon_sonuclari.sort(key=lambda x: (x[0], -abs(x[1] - int(_ed50_zone))), reverse=True)
                                    _en_iyi_icerde, _en_iyi_zon, _en_iyi_noktalar, _en_iyi_uyarilar, _en_iyi_ozet = _zon_sonuclari[0]
                                    if _en_iyi_icerde > 0:
                                        _otomatik_ed50_zone = int(_en_iyi_zon)
                                        _excel_noktalar = _en_iyi_noktalar
                                        _excel_uyarilar = _en_iyi_uyarilar
                                        _excel_ozet = _en_iyi_ozet
                                        if _otomatik_ed50_zone != int(_ed50_zone):
                                            st.info(
                                                f"ED50 UTM zonu otomatik düzeltildi: {_ed50_zone}N → "
                                                f"{_otomatik_ed50_zone}N. Santral sınırıyla eşleşen zon kullanıldı."
                                            )
                                            app_state["manual_turbine_ed50_zone"] = _otomatik_ed50_zone

                            if not _excel_noktalar:
                                st.warning("Excel/CSV içinde geçerli türbin koordinatı bulunamadı.")
                            else:
                                _saha_ici = []
                                _saha_disi = 0
                                for _n in _excel_noktalar:
                                    _k = dict(_n)
                                    _k["excel_lat"] = float(_k["lat"])
                                    _k["excel_lon"] = float(_k["lon"])
                                    _saha_ici.append(_k)
                                app_state["manual_turbine_points"] = _saha_ici
                                app_state["manual_turbine_excel_name"] = _excel_imza
                                app_state["turbine_layout"] = None
                                app_state["wake_result"] = None
                                app_state["production_result"] = None
                                kalici_durumu_kaydet(app_state)

                                if _excel_ozet:
                                    _zon_notu = (
                                        f" · Otomatik zon: {_otomatik_ed50_zone}N"
                                        if _otomatik_ed50_zone is not None else ""
                                    )
                                    st.success(
                                        f"{len(_saha_ici)} türbin Excel/CSV'den okundu ve yerleşime aktarıldı. "
                                        f"Kaynak: {_excel_ozet['source_crs']} → WGS84{_zon_notu}. "
                                        f"Algılanan sütunlar: {_excel_ozet['x_col']} / {_excel_ozet['y_col']}."
                                    )
                                for _u in _excel_uyarilar[:8]:
                                    st.caption("• " + _u)
                                st.rerun()
                        except Exception as _excel_hata:
                            st.error(str(_excel_hata))

                _manuel_noktalar = list(app_state.get("manual_turbine_points", []) or [])

                st.markdown("##### Türbinleri düzenle")
                _ekle_col1, _ekle_col2 = st.columns(2)
                with _ekle_col1:
                    _ekleme_aktif = st.toggle(
                        "Türbin ekle modu",
                        value=bool(app_state.get("manual_turbine_add_mode", False)),
                        key="manuel_turbin_ekle_toggle_v1103",
                        help="Açıkken sağdaki rüzgâr haritasına tıklayarak yeni türbin eklersiniz.",
                    )
                with _ekle_col2:
                    _tek_turbin_ekle = st.button(
                        "+ 1 türbin ekle",
                        use_container_width=True,
                        key="manuel_tek_turbin_ekle_v1103",
                    )

                app_state["manual_turbine_add_mode"] = bool(_ekleme_aktif)

                if _tek_turbin_ekle:
                    _sinir_pol = None
                    try:
                        _sinir_dosyasi = kayitli_dosyayi_olustur(app_state.get("santral_boundary"))
                        if _sinir_dosyasi is not None:
                            _sinir_pol = kml_kmz_sinirlarini_oku(_sinir_dosyasi)
                    except Exception:
                        _sinir_pol = None
                    _pts = list(app_state.get("manual_turbine_points", []) or [])
                    if _sinir_pol:
                        _pts = eksik_turbinleri_sahaya_ekle(_pts, len(_pts) + 1, _sinir_pol)
                        app_state["manual_turbine_points"] = _pts
                        app_state["turbine_count"] = max(int(app_state.get("turbine_count", 1) or 1), len(_pts))
                        app_state["turbine_layout"] = None
                        app_state["wake_result"] = None
                        app_state["production_result"] = None
                        kalici_durumu_kaydet(app_state)
                        st.rerun()

                if _ekleme_aktif:
                    st.success("Ekleme modu açık · Rüzgâr haritasında istediğiniz saha noktasına tıklayın.")
                else:
                    st.caption(
                        "Excel türbinini kaydırmak için aşağıdan türbini seçin veya haritadaki türbin noktasına tıklayın."
                    )

                _m1, _m2 = st.columns(2)
                _m1.metric("Toplam manuel / Excel türbini", len(_manuel_noktalar))
                if _m2.button(
                    "Son türbini sil",
                    key="manuel_son_turbini_sil_v1101",
                    use_container_width=True,
                ):
                    if _manuel_noktalar:
                        _manuel_noktalar = _manuel_noktalar[:-1]
                        app_state["manual_turbine_points"] = _manuel_noktalar
                        app_state["manual_turbine_selected_index"] = max(0, len(_manuel_noktalar) - 1)
                        app_state["turbine_layout"] = None
                        app_state["wake_result"] = None
                        app_state["production_result"] = None
                        kalici_durumu_kaydet(app_state)
                        st.rerun()

                if _manuel_noktalar:
                    st.info(
                        "Excel'den gelen türbinleri sağdaki haritada fareyle tutup sürükleyerek "
                        "istediğiniz konuma bırakabilirsiniz. Bırakılan konum wake ve AEP "
                        "hesabına otomatik aktarılır."
                    )

                if st.button(
                    "Tüm manuel / Excel türbinlerini temizle",
                    key="manuel_turbinleri_temizle_v1101",
                    use_container_width=True,
                ):
                    app_state["manual_turbine_points"] = []
                    app_state["manual_turbine_excel_name"] = ""
                    app_state["manual_turbine_selected_index"] = 0
                    app_state["manual_turbine_add_mode"] = False
                    app_state["turbine_layout"] = None
                    app_state["wake_result"] = None
                    app_state["production_result"] = None
                    kalici_durumu_kaydet(app_state)
                    st.rerun()

                manuel_koordinatlar = ""
            else:
                manuel_koordinatlar = ""

            st.markdown("##### Yerleşim kuralları")
            capraz_mesafe_d = st.number_input(
                "Hakim rüzgara dik mesafe (D)",
                min_value=1.0,
                max_value=10.0,
                value=float(app_state.get("crosswind_spacing_d", 2.5)),
                step=0.1,
                key="capraz_mesafe_d_widget"
            )
            app_state["crosswind_spacing_d"] = float(capraz_mesafe_d)
            ruzgar_alti_mesafe_d = st.number_input(
                "Hakim rüzgar yönünde mesafe (D)",
                min_value=2.0,
                max_value=15.0,
                value=float(app_state.get("downwind_spacing_d", 6.0)),
                step=0.5,
                key="ruzgar_alti_mesafe_d_widget"
            )
            app_state["downwind_spacing_d"] = float(ruzgar_alti_mesafe_d)
            otomatik_yon = hakim_ruzgar_yonu_hesapla(temiz_veri)
            yerlesim_yonu = st.number_input(
                "Hakim rüzgar geliş yönü (°)",
                min_value=0.0,
                max_value=359.9,
                value=float(app_state.get("dominant_wind_direction") if app_state.get("dominant_wind_direction") is not None else round(otomatik_yon, 1)),
                step=1.0,
                key="yerlesim_yonu_widget"
            )
            app_state["dominant_wind_direction"] = float(yerlesim_yonu)
            setback_m = st.number_input(
                "Sınırdan geri çekilme (m)",
                min_value=0.0,
                max_value=3000.0,
                value=float(app_state.get("setback", 0.0)),
                step=25.0,
                key="setback_m_widget"
            )
            app_state["setback"] = float(setback_m)

            st.caption(
                f"Rotor: {model_bilgisi['rotor_capi_m']} m | "
                f"Elips kriteri: {capraz_mesafe_d:.1f}D × {ruzgar_alti_mesafe_d:.1f}D"
            )

        with turbin_sag:
            turbin_harita_alani = st.container()

    # --------------------------------------------------------
    # ORTAK HESAPLAR
    # --------------------------------------------------------
    kayip_senaryosu = app_state.get("loss_scenario", "P50")
    if kayip_senaryosu not in KAYIP_SENARYOLARI:
        kayip_senaryosu = "P50"
    kayiplar = KAYIP_SENARYOLARI[kayip_senaryosu]

    sonuc = turbin_uretimi_coklu_direk_hesapla(
        secili_filtreli_veriler,
        app_state["sensor_heights"],
        model_bilgisi,
        hub_yuksekligi,
        int(turbin_sayisi),
        kayiplar
    )
    aep_hazir = sonuc is not None
    if not aep_hazir:
        st.warning(
            "Rüzgar direği/koordinatı seçilmediği için AEP hesabı beklemede. "
            "Santral sınırı yine de haritada açılacaktır."
        )

    yerlesim_turbinleri = []
    layout_wake_kaybi = 0.0
    wake_tablo = []
    kullanilan_grid = pd.DataFrame()
    yerlesim_gridi = pd.DataFrame()
    santral_poligonu = None
    calisma_poligonu = None
    yasak_poligonlar = []
    harita_hatasi = None
    harita_kaynagi = ""
    direk_dogrulama_tablo = []
    referans_saha_hizi = np.nan
    ortak_baslangic = None
    ortak_bitis = None

    if santral_siniri is not None:
        try:
            santral_poligonu = kml_kmz_sinirlarini_oku(santral_siniri)
            calisma_poligonu = kare_calisma_alani_uret(
                santral_poligonu, app_state.get("wind_map_area_km", 10.0),
                merkez_konum=app_state.get("wind_map_center")
            )
            yasak_poligonlar = (
                kml_kmz_tum_poligonlari_oku(yasak_alan_dosyasi)
                if yasak_alan_dosyasi else []
            )

            direk_noktalari = []

            # Seçili direkleri mümkün olduğunca aynı ölçüm döneminde karşılaştır.
            ortak_baslangic = None
            ortak_bitis = None
            _zaman_araliklari = []
            for _ad, _veri in secili_filtreli_veriler.items():
                if "TIMESTAMP" not in _veri.columns or _veri.empty:
                    continue
                _ts = pd.to_datetime(_veri["TIMESTAMP"], errors="coerce").dropna()
                if not _ts.empty:
                    _zaman_araliklari.append((_ts.min(), _ts.max()))
            if _zaman_araliklari:
                ortak_baslangic = max(x[0] for x in _zaman_araliklari)
                ortak_bitis = min(x[1] for x in _zaman_araliklari)
                if ortak_baslangic >= ortak_bitis:
                    ortak_baslangic = None
                    ortak_bitis = None

            eksik_koordinatli_direkler = [
                ad for ad in secili_filtreli_veriler if ad not in direk_koordinatlari
            ]

            for dosya_adi, tum_veri in secili_filtreli_veriler.items():
                if dosya_adi not in direk_koordinatlari:
                    continue
                kullanilan_lat = float(direk_koordinatlari[dosya_adi]["lat"])
                kullanilan_lon = float(direk_koordinatlari[dosya_adi]["lon"])

                dosya_yukseklikleri = app_state["sensor_heights"].get(
                    dosya_adi,
                    VARSAYILAN_SENSOR_YUKSEKLIKLERI
                ) or {}
                dosya_yukseklik_tuple = sensor_yukseklik_tuple(dosya_yukseklikleri)
                analiz_verisi = tum_veri
                if ortak_baslangic is not None and ortak_bitis is not None and "TIMESTAMP" in tum_veri.columns:
                    analiz_verisi = tum_veri[(tum_veri["TIMESTAMP"] >= ortak_baslangic) & (tum_veri["TIMESTAMP"] <= ortak_bitis)].copy()
                    if analiz_verisi.empty:
                        analiz_verisi = tum_veri
                temiz_tum = olcum_kalite_verisi(analiz_verisi, dosya_adi)
                alpha_tum, _ = saha_alpha_hesapla(temiz_tum, dosya_yukseklik_tuple)

                # WS1'e körü körüne güvenme: veri kolonu bulunan en yüksek geçerli sensörü seç.
                _aday_sensorler = []
                for _kolon in RUZGAR_KOLONLARI:
                    try:
                        _yuk = float(dosya_yukseklikleri.get(_kolon, 0.0) or 0.0)
                    except (TypeError, ValueError):
                        _yuk = 0.0
                    if _kolon in temiz_tum.columns and np.isfinite(_yuk) and _yuk > 0:
                        _ort = pd.to_numeric(temiz_tum[_kolon], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().mean()
                        if np.isfinite(_ort) and _ort > 0:
                            _aday_sensorler.append((_yuk, _kolon, float(_ort)))
                if not _aday_sensorler:
                    continue
                ref_yukseklik, ref_kolon, ref = max(_aday_sensorler, key=lambda x: x[0])
                oran = float(hub_yuksekligi) / float(ref_yukseklik)
                if not np.isfinite(oran) or oran <= 0:
                    continue
                hub_hizi = float(ref * (oran ** float(alpha_tum)))
                if not np.isfinite(hub_hizi) or hub_hizi <= 0:
                    continue
                _gecerli_sayisi = int(pd.to_numeric(temiz_tum[ref_kolon], errors="coerce").notna().sum())
                _toplam_sayisi = max(int(len(analiz_verisi)), 1)
                _veri_tamligi = float(np.clip(_gecerli_sayisi / _toplam_sayisi, 0.05, 1.0))
                direk_noktalari.append({
                    "ad": veri_seti_gorunur_adi(dosya_adi),
                    "veri_seti": dosya_adi,
                    "lat": kullanilan_lat,
                    "lon": kullanilan_lon,
                    "hub_hizi": hub_hizi,
                    "referans_sensor": ref_kolon,
                    "referans_yukseklik": float(ref_yukseklik),
                    "veri_tamligi": _veri_tamligi,
                    "agirlik": max(0.10, _veri_tamligi),
                    "ortak_donem_baslangic": ortak_baslangic,
                    "ortak_donem_bitis": ortak_bitis,
                })

            if direk_noktalari:
                _mast_hiz = np.array([d["hub_hizi"] for d in direk_noktalari], dtype=float)
                _mast_agirlik = np.array([d.get("agirlik", 1.0) for d in direk_noktalari], dtype=float)
                referans_saha_hizi = float(np.average(_mast_hiz, weights=_mast_agirlik))
                with st.spinner("Global Wind Atlas verisi hazırlanıyor ve ölçüm direkleriyle kalibre ediliyor..."):
                    ham_grid = _gwa_ruzg_haritasi_uret(
                        calisma_poligonu,
                        direk_noktalari,
                        tif_kaydi=None,
                        api_url="",
                        gwa_yukseklik_m=int(app_state.get("gwa_height_m", 100)),
                        hub_yuksekligi=float(hub_yuksekligi),
                        grid_boyutu=int(app_state.get("wind_map_grid_density", 60)),
                        kalibre_et=True,
                    )
                harita_kaynagi = f"Global Wind Atlas 4.0 · Mean Wind Speed @{int(app_state.get('gwa_height_m',100))} m + direk kalibrasyonu"
                # Harita, kullanıcı tarafından belirlenen kare çalışma alanının tamamını gösterir.
                kullanilan_grid = ham_grid.copy()
                # Türbin yerleşimi ise güvenlik için yalnız santral sınırı ve mevcut filtrelerle sınırlıdır.
                yerlesim_gridi = grid_saha_filtrele(
                    ham_grid,
                    santral_poligonu,
                    yasak_poligonlar,
                    setback_m=setback_m,
                    max_egim_deg=None
                )
            else:
                ham_grid = pd.DataFrame()
                kullanilan_grid = pd.DataFrame()
                yerlesim_gridi = pd.DataFrame()
                harita_kaynagi = "Santral sınırı önizlemesi · rüzgar direği seçimi bekleniyor"
            _arazi_etiketi = "Global Wind Atlas 4.0"
            if direk_noktalari:
                harita_kaynagi = f"Global Wind Atlas 4.0 · Mean Wind Speed @{int(app_state.get('gwa_height_m',100))} m + direk kalibrasyonu"

            harita_koordinat_uyarisi = None
            if eksik_koordinatli_direkler:
                harita_koordinat_uyarisi = (
                    "Koordinatı girilmediği için haritaya dahil edilmeyen seçili direk(ler): "
                    + ", ".join(eksik_koordinatli_direkler)
                )

            # Küçük/dar sahalarda yüksek setback bütün grid hücrelerini silebilir.
            # Uygulamayı durdurmak yerine güvenli kademeli geri dönüş uygula.
            harita_filtre_uyarisi = None
            if yerlesim_gridi.empty and not ham_grid.empty and float(setback_m) > 0:
                yerlesim_gridi = grid_saha_filtrele(
                    ham_grid,
                    santral_poligonu,
                    yasak_poligonlar,
                    setback_m=0.0,
                    max_egim_deg=None
                )
                if not yerlesim_gridi.empty:
                    harita_filtre_uyarisi = (
                        f"Girilen {float(setback_m):g} m setback bu saha için bütün harita "
                        "hücrelerini kaldırdığı için türbin yerleşim gridi setback uygulanmadan gösterildi."
                    )

            if yerlesim_gridi.empty and not ham_grid.empty and yasak_poligonlar:
                yerlesim_gridi = grid_saha_filtrele(
                    ham_grid,
                    santral_poligonu,
                    [],
                    setback_m=0.0,
                    max_egim_deg=None
                )
                if not yerlesim_gridi.empty:
                    harita_filtre_uyarisi = (
                        "Yasak alan ve setback filtreleri bütün harita hücrelerini kaldırdığı için "
                        "türbin yerleşim gridi yalnızca ana santral sınırıyla gösterildi."
                    )

            # Son güvenli geri dönüş: ham grid zaten ana poligon içinde üretilir.
            if yerlesim_gridi.empty and not ham_grid.empty:
                yerlesim_gridi = ham_grid.copy()
                harita_filtre_uyarisi = (
                    "Filtrelerden sonra hücre kalmadığı için türbin yerleşim gridi ana santral sınırı "
                    "içindeki ham grid üzerinden gösterildi."
                )

            direk_dogrulama_tablo = []
            if not ham_grid.empty and direk_noktalari:
                for _d in direk_noktalari:
                    _mesafe2 = (ham_grid["lat"] - float(_d["lat"])) ** 2 + (ham_grid["lon"] - float(_d["lon"])) ** 2
                    _idx = _mesafe2.idxmin()
                    _model = float(ham_grid.loc[_idx, "Hub Rüzgar Hızı (m/s)"])
                    _olcum = float(_d["hub_hizi"])
                    direk_dogrulama_tablo.append({
                        "Direk": _d["ad"],
                        "Ölçüm / hedef yükseklik (m/s)": _olcum,
                        "Harita tahmini (m/s)": _model,
                        "Fark (m/s)": _model - _olcum,
                        "Mutlak hata (%)": abs(_model - _olcum) / _olcum * 100.0 if _olcum > 0 else np.nan,
                        "Veri tamlığı (%)": 100.0 * float(_d.get("veri_tamligi", 1.0)),
                    })

            manuel_yerlesim_uyarilari = []
            if app_state.get("turbine_placement_mode") == "Manuel / Excel yerleşimi":
                yerlesim_turbinleri, manuel_yerlesim_uyarilari = haritadan_turbin_yerlesimi_uret(
                    app_state.get("manual_turbine_points", []),
                    santral_poligonu,
                    yerlesim_yonu,
                    grid=yerlesim_gridi if not yerlesim_gridi.empty else kullanilan_grid,
                )
            elif not yerlesim_gridi.empty:
                yerlesim_turbinleri = micrositing_yerlesimi_uret(
                    yerlesim_gridi,
                    santral_poligonu,
                    int(turbin_sayisi),
                    model_bilgisi["rotor_capi_m"],
                    yerlesim_yonu,
                    capraz_d=capraz_mesafe_d,
                    ruzgar_alti_d=ruzgar_alti_mesafe_d
                )

            if yerlesim_turbinleri:
                wake_tablo, layout_wake_kaybi = jensen_wake_kaybi_hesapla(
                    yerlesim_turbinleri,
                    model_bilgisi["rotor_capi_m"]
                )
        except Exception as hata:
            harita_hatasi = str(hata)

    # --------------------------------------------------------
    # HARİTA ÇİZİM YARDIMCISI
    # --------------------------------------------------------
    def harita_ciz(turbinleri_goster=False, yukseklik=570, grafik_anahtari="ruzgar_haritasi", nokta_secimi=False):
        if santral_siniri is None:
            st.info("Santral sınırını KML/KMZ olarak yükleyin.")
            return
        if harita_hatasi:
            st.error(f"Rüzgar haritası oluşturulamadı: {harita_hatasi}")
            return
        sinir_only = kullanilan_grid.empty
        if sinir_only:
            st.info(
                "Santral sınırı açıldı. Rüzgar alanını üretmek için en az bir direği seçip "
                "koordinatını girin; sınır ve kayıtlı direkler aşağıda yine gösterilir."
            )
        if 'harita_koordinat_uyarisi' in locals() and harita_koordinat_uyarisi:
            st.warning(harita_koordinat_uyarisi)
        if 'harita_filtre_uyarisi' in locals() and harita_filtre_uyarisi:
            st.warning(harita_filtre_uyarisi)

        lejant_goster = False

        renk_skala = [
            [0.0, "#173bff"],
            [0.35, "#12cfff"],
            [0.60, "#20e86b"],
            [0.82, "#e9f52f"],
            [1.0, "#ff9a1f"]
        ]

        harita = go.Figure()
        ruzgar_yuzeyi_katmani = None
        surukle_wind_overlay = None
        if not kullanilan_grid.empty:
            hiz_min = float(kullanilan_grid["Hub Rüzgar Hızı (m/s)"].min())
            hiz_max = float(kullanilan_grid["Hub Rüzgar Hızı (m/s)"].max())
            hiz_orta = (hiz_min + hiz_max) / 2.0

            # Nokta görünümü yerine topoğrafyayı izleyen, kademeli kontur bantlı
            # sürekli bir rüzgâr yüzeyi üret. Ortalama rüzgâr hızı korunur;
            # yalnızca grid içindeki mekânsal ayrıntı DEM/sırt/eğim bilgisiyle güçlendirilir.
            try:
                from PIL import Image
                import matplotlib.colors as mcolors
                from scipy.ndimage import distance_transform_edt, gaussian_filter, zoom

                lon_degerleri = np.sort(kullanilan_grid["lon"].astype(float).unique())
                lat_degerleri = np.sort(kullanilan_grid["lat"].astype(float).unique())

                def _pivot_matris(kolon):
                    if kolon not in kullanilan_grid.columns:
                        return None
                    return (
                        kullanilan_grid.pivot_table(
                            index="lat", columns="lon", values=kolon, aggfunc="mean"
                        )
                        .reindex(index=lat_degerleri, columns=lon_degerleri)
                        .to_numpy(dtype=float)
                    )

                def _eksik_doldur(mat):
                    if mat is None:
                        return None
                    mat = np.asarray(mat, dtype=float)
                    if np.isfinite(mat).all():
                        return mat
                    if not np.isfinite(mat).any():
                        return np.zeros_like(mat, dtype=float)
                    eksik = ~np.isfinite(mat)
                    indisler = distance_transform_edt(
                        eksik, return_distances=False, return_indices=True
                    )
                    return mat[tuple(indisler)]

                hiz_mat = _eksik_doldur(_pivot_matris("Hub Rüzgar Hızı (m/s)"))
                kot_mat = _eksik_doldur(_pivot_matris("Kot (m)"))
                sirt_mat = _eksik_doldur(_pivot_matris("Sırtlık İndeksi"))
                egim_mat = _eksik_doldur(_pivot_matris("Yönlü Eğim"))

                if hiz_mat is None or hiz_mat.size == 0:
                    raise ValueError("Rüzgâr grid matrisi oluşturulamadı.")

                def _robust_norm(mat):
                    mat = np.asarray(mat, dtype=float)
                    g = mat[np.isfinite(mat)]
                    if g.size < 2:
                        return np.zeros_like(mat)
                    lo, hi = np.nanpercentile(g, [5, 95])
                    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
                        return np.zeros_like(mat)
                    return np.clip((mat - lo) / (hi - lo), 0.0, 1.0) * 2.0 - 1.0

                # SAYISAL DEĞER KORUMA:
                # Görsel harita için yeni hız üretme, DEM ayrıntısı ekleme veya ortalamayı
                # yeniden dağıtma yapılmaz. Renk yüzeyi doğrudan hesaplanan
                # "Hub Rüzgar Hızı (m/s)" gridinden oluşturulur. Böylece aynı koordinatta
                # hover değeri ile renk sınıfı aynı sayısal değeri temsil eder.
                gorsel_hiz = np.asarray(hiz_mat, dtype=float).copy()

                hedef_px = 1000
                zoom_y = max(1.0, hedef_px / max(gorsel_hiz.shape[0], 1))
                zoom_x = max(1.0, hedef_px / max(gorsel_hiz.shape[1], 1))
                # Bilinear büyütme yalnızca pikseller arasındaki geçişi doldurur;
                # orijinal grid düğümlerindeki hız değerleri değiştirilmez.
                buyuk = zoom(gorsel_hiz, (zoom_y, zoom_x), order=1, prefilter=False)

                # İkinci örnekteki topoğrafik harita görünümü için sürekli gradyan
                # yerine sık kontur bantları kullanılır.
                vmin = float(np.nanpercentile(buyuk, 1))
                vmax = float(np.nanpercentile(buyuk, 99))
                if vmax <= vmin:
                    vmax = vmin + 0.01
                bant_sayisi = 24
                seviyeler = np.linspace(vmin, vmax, bant_sayisi + 1)
                bant = np.digitize(buyuk, seviyeler[1:-1], right=False)
                bant_norm = bant.astype(float) / max(bant_sayisi - 1, 1)

                renk_skala_topo = [
                    (0.00, "#5527cf"),
                    (0.12, "#2738e8"),
                    (0.28, "#178df2"),
                    (0.43, "#22d7ed"),
                    (0.57, "#55e7be"),
                    (0.70, "#35df62"),
                    (0.84, "#baf238"),
                    (0.94, "#fff044"),
                    (1.00, "#ff9f24"),
                ]
                cmap = mcolors.LinearSegmentedColormap.from_list("maki_topo_wind", renk_skala_topo)
                rgba = (cmap(bant_norm) * 255).astype(np.uint8)

                # Kontur bant sınırlarını çok hafif koyulaştır; nokta görünümü oluşmaz.
                sinir = np.zeros(bant.shape, dtype=bool)
                sinir[1:, :] |= bant[1:, :] != bant[:-1, :]
                sinir[:, 1:] |= bant[:, 1:] != bant[:, :-1]
                sinir = gaussian_filter(sinir.astype(float), sigma=0.45) > 0.18
                rgba[sinir, :3] = (rgba[sinir, :3].astype(float) * 0.84).astype(np.uint8)
                rgba[..., 3] = 218

                # Plotly image layer kuzey-batıdan başladığı için matrisi ters çevir.
                rgba = np.flipud(rgba)
                goruntu = Image.fromarray(rgba, mode="RGBA")
                tampon = io.BytesIO()
                goruntu.save(tampon, format="PNG", optimize=True)
                kaynak_uri = "data:image/png;base64," + base64.b64encode(tampon.getvalue()).decode("ascii")

                lon_min, lon_max = float(lon_degerleri.min()), float(lon_degerleri.max())
                lat_min, lat_max = float(lat_degerleri.min()), float(lat_degerleri.max())
                ruzgar_yuzeyi_katmani = dict(
                    sourcetype="image",
                    source=kaynak_uri,
                    coordinates=[
                        [lon_min, lat_max], [lon_max, lat_max],
                        [lon_max, lat_min], [lon_min, lat_min]
                    ],
                    opacity=0.88,
                    below="traces",
                )
                try:
                    _wo_coords = ruzgar_yuzeyi_katmani.get("coordinates") or []
                    if len(_wo_coords) >= 4:
                        _wo_lons = [float(p[0]) for p in _wo_coords]
                        _wo_lats = [float(p[1]) for p in _wo_coords]
                        surukle_wind_overlay = {
                            "image": kaynak_uri,
                            "bounds": [
                                [min(_wo_lats), min(_wo_lons)],
                                [max(_wo_lats), max(_wo_lons)],
                            ],
                        }
                except Exception:
                    surukle_wind_overlay = None


                # Hover değerleri hesaplanan gerçek grid hızından gelir; görsel banttan değil.
                hover_grid = kullanilan_grid.iloc[::max(1, len(kullanilan_grid) // 1200)].copy()
                harita.add_trace(go.Scattermap(
                    lat=hover_grid["lat"], lon=hover_grid["lon"], mode="markers",
                    marker=dict(size=11, opacity=0.001),
                    customdata=hover_grid[["Hub Rüzgar Hızı (m/s)"]].to_numpy(),
                    hovertemplate="Hub hızı: %{customdata[0]:.2f} m/s<extra></extra>",
                    name="Rüzgâr yüzeyi", showlegend=False,
                ))
            except Exception as yuzey_hatasi:
                # Görsel raster üretilemezse uygulama durmaz; mevcut yoğun nokta
                # gösterimine yalnızca güvenli geri dönüş yapılır.
                harita.add_trace(go.Scattermap(
                    lat=kullanilan_grid["lat"], lon=kullanilan_grid["lon"],
                    mode="markers",
                    marker=dict(
                        size=6, color=kullanilan_grid["Hub Rüzgar Hızı (m/s)"],
                        colorscale=renk_skala, cmin=hiz_min, cmax=hiz_max,
                        opacity=0.82, showscale=False,
                    ),
                    customdata=kullanilan_grid[["Hub Rüzgar Hızı (m/s)"]].to_numpy(),
                    hovertemplate="Hub hızı: %{customdata[0]:.2f} m/s<extra></extra>",
                    name=f"Rüzgâr yüzeyi geri dönüşü ({type(yuzey_hatasi).__name__})",
                    showlegend=False,
                ))

        pol_lon = [p[0] for p in santral_poligonu]
        pol_lat = [p[1] for p in santral_poligonu]
        if calisma_poligonu:
            harita.add_trace(go.Scattermap(
                lat=[p[1] for p in calisma_poligonu],
                lon=[p[0] for p in calisma_poligonu],
                mode="lines",
                line=dict(width=2, color="rgba(255,165,0,0.95)"),
                name="Rüzgâr haritası çalışma alanı"
            ))
        harita.add_trace(go.Scattermap(
            lat=pol_lat,
            lon=pol_lon,
            mode="lines",
            line=dict(width=3),
            name="Santral sınırı"
        ))

        # KMZ açıldığı anda koordinatı kayıtlı ölçüm direklerini de göster.
        _harita_direkleri = []
        for _ad, _konum in direk_koordinatlari.items():
            try:
                _lat, _lon = float(_konum["lat"]), float(_konum["lon"])
                if _lat != 0.0 or _lon != 0.0:
                    _harita_direkleri.append((_ad, _lat, _lon))
            except Exception:
                pass
        if _harita_direkleri:
            harita.add_trace(go.Scattermap(
                lat=[d[1] for d in _harita_direkleri],
                lon=[d[2] for d in _harita_direkleri],
                mode="markers+text",
                marker=dict(size=18, symbol="circle"),
                text=["📡 " + d[0] for d in _harita_direkleri],
                textposition="top center",
                hovertemplate="%{text}<br>Enlem: %{lat:.6f}<br>Boylam: %{lon:.6f}<extra></extra>",
                name="Rüzgar direkleri"
            ))

        for idx, yasak in enumerate(yasak_poligonlar, 1):
            harita.add_trace(go.Scattermap(
                lat=[p[1] for p in yasak],
                lon=[p[0] for p in yasak],
                mode="lines",
                line=dict(width=3),
                name=f"Yasak alan {idx}"
            ))

        if turbinleri_goster and yerlesim_turbinleri:
            elips_lat, elips_lon = turbin_elips_cizgileri_uret(
                yerlesim_turbinleri,
                santral_poligonu,
                model_bilgisi["rotor_capi_m"],
                yerlesim_yonu,
                capraz_d=capraz_mesafe_d,
                ruzgar_alti_d=ruzgar_alti_mesafe_d
            )
            harita.add_trace(go.Scattermap(
                lat=elips_lat,
                lon=elips_lon,
                mode="lines",
                line=dict(width=2, color="rgba(220, 30, 30, 0.65)"),
                hoverinfo="skip",
                name=f"{capraz_mesafe_d:.1f}D × {ruzgar_alti_mesafe_d:.1f}D elipsleri"
            ))

            _turbin_customdata = [
                ["TURBINE_EXISTING", i, t.get("hub_hizi", np.nan)]
                for i, t in enumerate(yerlesim_turbinleri)
            ]
            harita.add_trace(go.Scattermap(
                lat=[t["lat"] for t in yerlesim_turbinleri],
                lon=[t["lon"] for t in yerlesim_turbinleri],
                mode="markers+text",
                marker=dict(size=16),
                text=[t["ad"] for t in yerlesim_turbinleri],
                textposition="top center",
                customdata=_turbin_customdata,
                hovertemplate=(
                    "%{text}<br>Yerel hız: %{customdata[2]:.2f} m/s"
                    "<br>Seçmek için noktaya tıklayın"
                    "<extra></extra>"
                ),
                name="Türbinler"
            ))


        # Haritadan manuel türbin seçimi: kullanıcı en yakın rüzgâr grid düğümüne tıklar.
        # Noktalar görünmezdir; tıklama yalnız koordinat seçmek için kullanılır.
        _turbin_ekleme_aktif = bool(app_state.get("manual_turbine_add_mode", False))
        if nokta_secimi and _turbin_ekleme_aktif and not kullanilan_grid.empty:
            _secim_grid = kullanilan_grid.copy()
            _secim_grid = _secim_grid.dropna(subset=["lat", "lon"])
            harita.add_trace(go.Scattermap(
                lat=_secim_grid["lat"].astype(float),
                lon=_secim_grid["lon"].astype(float),
                mode="markers",
                marker=dict(size=15, opacity=0.012),
                customdata=np.column_stack([
                    np.repeat("TURBINE_PICK", len(_secim_grid)),
                    _secim_grid["lat"].astype(float).to_numpy(),
                    _secim_grid["lon"].astype(float).to_numpy(),
                    _secim_grid["Hub Rüzgar Hızı (m/s)"].astype(float).to_numpy()
                    if "Hub Rüzgar Hızı (m/s)" in _secim_grid.columns
                    else np.full(len(_secim_grid), np.nan),
                ]),
                hovertemplate=(
                    "Türbin noktası seç<br>Enlem: %{lat:.6f}<br>Boylam: %{lon:.6f}"
                    "<extra></extra>"
                ),
                name="Türbin noktası seç",
                showlegend=False,
            ))

        harita.update_layout(
            map=dict(
                style="white-bg",
                layers=(
                    [dict(
                        below="traces",
                        sourcetype="raster",
                        source=["https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"]
                    )]
                    + ([ruzgar_yuzeyi_katmani] if ruzgar_yuzeyi_katmani else [])
                ),
                center=dict(
                    lat=float(np.mean([p[1] for p in (calisma_poligonu or santral_poligonu)])),
                    lon=float(np.mean([p[0] for p in (calisma_poligonu or santral_poligonu)]))
                ),
                zoom=float(np.clip(13.0 - np.log2(max(float(app_state.get("wind_map_area_km", 10.0)), 0.5)), 6.0, 12.5))
            ),
            height=yukseklik,
            margin=dict(l=0, r=0, t=10, b=0),
            clickmode="event+select" if nokta_secimi else "event",
            showlegend=lejant_goster,
            legend=dict(orientation="h")
        )
        if nokta_secimi:
            _secim_olayi = st.plotly_chart(
                harita,
                use_container_width=True,
                config={"displaylogo": False},
                key=grafik_anahtari,
                on_select="rerun",
                selection_mode="points",
            )
            try:
                _points = (_secim_olayi or {}).get("selection", {}).get("points", [])
            except Exception:
                try:
                    _points = getattr(getattr(_secim_olayi, "selection", None), "points", []) or []
                except Exception:
                    _points = []

            if _points:
                _p = _points[-1]
                _cd = _p.get("customdata") if isinstance(_p, dict) else getattr(_p, "customdata", None)
                if _cd:
                    _tip = str(_cd[0])

                    # Haritadaki mevcut türbine tıklanınca soldaki kaydırma aracı onu seçer.
                    if _tip == "TURBINE_EXISTING" and len(_cd) >= 2:
                        try:
                            _secili_idx = int(_cd[1])
                            _mevcut = list(app_state.get("manual_turbine_points", []) or [])
                            if 0 <= _secili_idx < len(_mevcut):
                                app_state["manual_turbine_selected_index"] = _secili_idx
                                kalici_durumu_kaydet(app_state)
                                st.rerun()
                        except Exception:
                            pass

                    # "Türbin ekle" modu açıkken görünmez grid üzerinden yeni nokta eklenir.
                    elif _tip == "TURBINE_PICK" and len(_cd) >= 3 and bool(app_state.get("manual_turbine_add_mode", False)):
                        try:
                            _lat = float(_cd[1]); _lon = float(_cd[2])
                            _mevcut = list(app_state.get("manual_turbine_points", []) or [])
                            _tekrar = any(
                                abs(float(q.get("lat", 999)) - _lat) < 1e-8
                                and abs(float(q.get("lon", 999)) - _lon) < 1e-8
                                for q in _mevcut
                            )

                            _tik_santral_poligonu = locals().get("santral_poligonu")
                            if not _tik_santral_poligonu:
                                try:
                                    _sinir_dosyasi = kayitli_dosyayi_olustur(app_state.get("santral_boundary"))
                                    if _sinir_dosyasi is not None:
                                        _tik_santral_poligonu = kml_kmz_sinirlarini_oku(_sinir_dosyasi)
                                except Exception:
                                    _tik_santral_poligonu = None

                            if (
                                not _tekrar
                                and _tik_santral_poligonu
                                and nokta_poligon_icinde(_lon, _lat, _tik_santral_poligonu)
                            ):
                                _mevcut.append({
                                    "lat": _lat,
                                    "lon": _lon,
                                    "ad": f"T{len(_mevcut) + 1}",
                                })
                                app_state["manual_turbine_points"] = _mevcut
                                app_state["manual_turbine_selected_index"] = len(_mevcut) - 1
                                app_state["turbine_layout"] = None
                                app_state["wake_result"] = None
                                app_state["production_result"] = None
                                kalici_durumu_kaydet(app_state)
                                st.rerun()
                        except Exception:
                            pass
        else:
            st.plotly_chart(
                harita,
                use_container_width=True,
                config={"displaylogo": False},
                key=grafik_anahtari
            )

    # Saha sekmesinin sağ tarafı: büyük haritada doğrudan çalışma karesi seçimi.
    with saha_harita_alani:
        if santral_siniri is not None:
            st.caption("BÜYÜK UYDU HARİTASI: Turuncu çalışma karesini tutup sürükleyin; bıraktığınız bölge yeniden hesaplanır. Boş zeminde haritayı kaydırın, fare tekerleğiyle yakınlaştırın.")
            try:
                _secim_poligon = kml_kmz_sinirlarini_oku(santral_siniri)
                _new_center = suruklenebilir_calisma_karesi(
                    _secim_poligon,
                    float(app_state.get("wind_map_area_km", 10.0)),
                    app_state.get("wind_map_center"),
                    key="maki_wind_square_BIG_v11115", height=570,
                )
                if isinstance(_new_center, dict) and _new_center.get("action") == "move":
                    _lat, _lon = float(_new_center["lat"]), float(_new_center["lon"])
                    if np.isfinite(_lat) and np.isfinite(_lon) and -85 < _lat < 85 and -180 < _lon < 180:
                        _old = app_state.get("wind_map_center")
                        if _old is None or abs(_lat-float(_old[0])) > 1e-6 or abs(_lon-float(_old[1])) > 1e-6:
                            app_state["wind_map_center"] = [_lat, _lon]
                            for _key in ("wind_grid", "turbine_layout", "wake_result", "production_result"):
                                app_state[_key] = None
                            st.rerun()
                if st.button("Çalışma karesini santral merkezine sıfırla", key="big_square_reset"):
                    app_state["wind_map_center"] = None
                    for _key in ("wind_grid", "turbine_layout", "wake_result", "production_result"):
                        app_state[_key] = None
                    st.rerun()
            except Exception as _map_error:
                st.error(f"Büyük harita açılamadı: {_map_error}")
        else:
            st.info("Büyük çalışma haritasını açmak için santral KMZ/KML sınırını yükleyin.")
        st.warning("GWA rasterının piksel doğruluğu henüz bağımsız referansla doğrulanmadı. Bu sürümde rüzgâr değerleri ve AEP yatırım kararı için onaylı değildir.")
        if False and not kullanilan_grid.empty:  # Doğrulanmamış raster sayısal çıktısı gizli
            _kaynak1 = str(kullanilan_grid["Arazi Veri Kaynağı"].iloc[0]) if "Arazi Veri Kaynağı" in kullanilan_grid.columns else "Bilinmiyor"
            _kaynak2 = str(kullanilan_grid["Pürüzlülük Veri Kaynağı"].iloc[0]) if "Pürüzlülük Veri Kaynağı" in kullanilan_grid.columns else "Bilinmiyor"
            _guven = float(kullanilan_grid["Model Güven Skoru"].mean()) if "Model Güven Skoru" in kullanilan_grid.columns else np.nan
            st.markdown("##### Saha ortalama rüzgâr hızı")
            _grid_ort = float(kullanilan_grid["Hub Rüzgar Hızı (m/s)"].mean()) if not kullanilan_grid.empty else np.nan
            st.metric(
                f"{float(app_state.get('wind_map_area_km', 10.0)):.1f} km × {float(app_state.get('wind_map_area_km', 10.0)):.1f} km çalışma alanı ortalaması",
                f"{_grid_ort:.2f} m/s" if np.isfinite(_grid_ort) else "—"
            )

    # Türbin sekmesinin sağ tarafını doldur.
    with turbin_harita_alani:
        _haritadan_secim_aktif = app_state.get("turbine_placement_mode") == "Manuel / Excel yerleşimi"

        if _haritadan_secim_aktif and santral_poligonu:
            _mevcut_drag_pts = list(app_state.get("manual_turbine_points", []) or [])
            _hedef_turbin_sayisi = int(app_state.get("turbine_count", len(_mevcut_drag_pts) or 1) or 1)

            # Kullanıcı Excel'deki 7 türbinden 8/9/10'a çıkarsa eksik türbinleri saha içine otomatik ekle.
            if _hedef_turbin_sayisi > len(_mevcut_drag_pts):
                _yeni_drag_pts = eksik_turbinleri_sahaya_ekle(
                    _mevcut_drag_pts,
                    _hedef_turbin_sayisi,
                    santral_poligonu,
                )
                if len(_yeni_drag_pts) != len(_mevcut_drag_pts):
                    app_state["manual_turbine_points"] = _yeni_drag_pts
                    app_state["turbine_layout"] = None
                    app_state["wake_result"] = None
                    app_state["production_result"] = None
                    kalici_durumu_kaydet(app_state)
                    _mevcut_drag_pts = _yeni_drag_pts

            st.caption(
                "Rüzgâr haritası ekranda kalır. Türbin noktasını fareyle tutup sürükleyin ve istediğiniz yerde bırakın. "
                "Türbin ekle modu açıksa boş bir noktaya tıklayarak yeni türbin ekleyebilirsiniz."
            )

            # Manuel modda rüzgâr yüzeyini bağımsız üret.
            # Önceki sürümde harita_ciz() içindeki yerel `surukle_wind_overlay`
            # değişkenine erişilmeye çalışıldığı için sağ taraf boş kalıyordu.
            _manuel_wind_overlay = surukle_ruzgar_overlay_uret(kullanilan_grid)

            _drag_sonuc = suruklenebilir_turbin_haritasi(
                santral_poligonu,
                _mevcut_drag_pts,
                add_mode=bool(app_state.get("manual_turbine_add_mode", False)),
                height=570,
                key="turbin_drag_editor_v1109",
                wind_overlay=_manuel_wind_overlay,
            )

            if isinstance(_drag_sonuc, dict) and _drag_sonuc.get("action") == "editor_error":
                st.warning("Sürükle-bırak editörü açılamadı; rüzgâr haritası normal görünümde gösteriliyor.")
                harita_ciz(
                    turbinleri_goster=True,
                    yukseklik=570,
                    grafik_anahtari="turbin_ruzgar_haritasi_fallback_v1105",
                    nokta_secimi=False,
                )

            if isinstance(_drag_sonuc, dict) and _drag_sonuc.get("action") == "update":
                _yeni_pts = _drag_sonuc.get("points") or []
                _eski_pts = app_state.get("manual_turbine_points", []) or []

                _degisti = len(_yeni_pts) != len(_eski_pts)
                if not _degisti and len(_yeni_pts) == len(_eski_pts):
                    for _a, _b in zip(_yeni_pts, _eski_pts):
                        try:
                            if (
                                abs(float(_a.get("lat")) - float(_b.get("lat"))) > 1e-9
                                or abs(float(_a.get("lon")) - float(_b.get("lon"))) > 1e-9
                            ):
                                _degisti = True
                                break
                        except Exception:
                            _degisti = True
                            break

                if _degisti:
                    _temiz_pts = []
                    for _i, _p in enumerate(_yeni_pts):
                        try:
                            _lat = float(_p.get("lat"))
                            _lon = float(_p.get("lon"))
                            if not nokta_poligon_icinde(_lon, _lat, santral_poligonu):
                                continue
                            _temiz_pts.append({
                                "lat": _lat,
                                "lon": _lon,
                                "ad": str(_p.get("ad") or f"T{_i+1}"),
                                "excel_lat": _p.get("excel_lat"),
                                "excel_lon": _p.get("excel_lon"),
                            })
                        except Exception:
                            continue

                    app_state["manual_turbine_points"] = _temiz_pts
                    app_state["turbine_count"] = max(1, len(_temiz_pts))
                    app_state["turbine_layout"] = None
                    app_state["wake_result"] = None
                    app_state["production_result"] = None
                    kalici_durumu_kaydet(app_state)
                    st.rerun()

        else:
            harita_ciz(
                turbinleri_goster=True,
                yukseklik=570,
                grafik_anahtari="turbin_ruzgar_haritasi_v1102",
                nokta_secimi=False,
            )
        if not kullanilan_grid.empty:
            if app_state.get("turbine_placement_mode") == "Manuel / Excel yerleşimi":
                for _uyari in locals().get("manuel_yerlesim_uyarilari", []):
                    st.warning(_uyari)
                if not yerlesim_turbinleri:
                    st.info("Türbin eklemek için sağdaki haritada santral sınırı içine tıklayın.")

            ozet1, ozet2, ozet3 = st.columns(3)
            _hedef_sayi_etiketi = (
                str(len(yerlesim_turbinleri))
                if app_state.get("turbine_placement_mode") == "Manuel / Excel yerleşimi"
                else f"{len(yerlesim_turbinleri)} / {int(turbin_sayisi)}"
            )
            ozet1.metric("Yerleştirilen türbin", _hedef_sayi_etiketi)
            ozet2.metric("Elips yarı eksenleri", f"{capraz_mesafe_d:.1f}D × {ruzgar_alti_mesafe_d:.1f}D")
            ozet3.metric("Ön wake kaybı", f"%{layout_wake_kaybi:.2f}")

            if (
                app_state.get("turbine_placement_mode") == "Otomatik yerleşim"
                and len(yerlesim_turbinleri) < int(turbin_sayisi)
            ):
                st.warning(
                    f"İstenen {int(turbin_sayisi)} türbinin {len(yerlesim_turbinleri)} adedi "
                    "sınır ve mesafe kriterlerini sağladı."
                )

            layout_df = turbin_layout_dataframe(yerlesim_turbinleri)
            if not layout_df.empty:
                with st.expander("Türbin koordinatları ve indirme"):
                    guvenli_dataframe(layout_df.round(5), use_container_width=True, hide_index=True)
                    st.download_button(
                        "Türbin yerleşimini CSV olarak indir",
                        data=layout_df.to_csv(index=False).encode("utf-8-sig"),
                        file_name="micrositing_turbin_yerlesimi.csv",
                        mime="text/csv",
                        key="layout_csv_v744"
                    )

    # --------------------------------------------------------
    # 3) ENERJİ ÜRETİMİ: AYAR VE SONUÇ AYNI SAYFADA
    # --------------------------------------------------------
    with sekme_sonuc:
        st.subheader("3 · Enerji Üretimi")
        if not aep_hazir:
            st.info("AEP sonucu için geçerli rüzgâr verisi ve saha sınırı gereklidir.")
            st.stop()

        # Sabit özet şeridi
        st.info(
            f"Saha: {SANTRAL} | Model: {model} | "
            f"{(len(yerlesim_turbinleri) if app_state.get('turbine_placement_mode') == 'Manuel koordinat girişi' and yerlesim_turbinleri else int(turbin_sayisi))} türbin | "
            f"Hub: {hub_yuksekligi:g} m | Senaryo: {kayip_senaryosu}"
        )
        st.caption(
            "Enerji sonucu ön-fizibilite AEP tahminidir; ölçüm verisi + hub yüksekliği dönüşümü + "
            "üretici güç eğrisi + tanımlı kayıp senaryolarını kullanır. Bankable enerji değerlendirmesi değildir."
        )
        st.caption("Yıllık ön tahmin yalnızca en az 365 gün, her ay ≥%90 geçerli ölçüm ve ≤2 saat en uzun boşluk koşullarıyla gösterilir. Takvim ayları gün sayılarıyla ağırlıklandırılır. Bu iç kontroller hub dönüşümünü, güç eğrisini, GWA veya uzun dönem iklimini doğrulamaz. P50/P75/P90 etiketleri mevcut kayıp paketlerinin adlarıdır; istatistiksel aşılma olasılığı hesabı yapılmıyor.")
        st.success(
            f"Gerçek temiz ölçümlerden güç eğrisi hesabı: {len(sonuc.get('kullanilan_direkler', []))} direk birlikte kullanıldı. "
            "Her direk kendi sensör yüksekliği ve shear değeriyle hub seviyesine taşındı; "
            "eşzamanlı hub hızlarının ortalaması güç eğrisine uygulandı."
        )

        ayar_col, sonuc_col = st.columns([0.30, 0.70], gap="large")
        with ayar_col:
            _kayip_secenekleri = list(KAYIP_SENARYOLARI.keys())
            _kayip_index = _kayip_secenekleri.index(app_state.get("loss_scenario", "P50")) if app_state.get("loss_scenario", "P50") in _kayip_secenekleri else 0
            kayip_senaryosu = st.selectbox(
                "Kayıp senaryosu",
                options=_kayip_secenekleri,
                index=_kayip_index,
                key="uretim_kayip_senaryosu_widget"
            )
            app_state["loss_scenario"] = kayip_senaryosu
            kayiplar = KAYIP_SENARYOLARI[kayip_senaryosu]
            _enerji_turbin_sayisi = (
                len(yerlesim_turbinleri)
                if app_state.get("turbine_placement_mode") == "Manuel / Excel yerleşimi" and yerlesim_turbinleri
                else int(turbin_sayisi)
            )
            sonuc = turbin_uretimi_coklu_direk_hesapla(
                secili_filtreli_veriler,
                app_state["sensor_heights"],
                model_bilgisi,
                hub_yuksekligi,
                int(_enerji_turbin_sayisi),
                kayiplar
            )
            if sonuc is None:
                st.error(
                    "Seçili direkte uygun zaman ekseni, geçerli ölçüm, sensör yüksekliği veya hub dönüşümü için en az 30 eşzamanlı kayıttan hesaplanabilir shear bulunamadı. "
                    "Kurulum raporu kaydını ve tarih aralığını kontrol edin."
                )
                st.stop()

            st.markdown("##### Senaryo kayıpları")
            st.write(f"Wake: %{kayiplar['wake']:.1f}")
            st.write(f"Kullanılabilirlik: %{kayiplar['kullanilabilirlik']:.1f}")
            st.write(f"Elektrik: %{kayiplar['elektrik']:.1f}")
            st.write(f"Diğer: %{kayiplar['diger']:.1f}")

        with sonuc_col:
            sonuc1, sonuc2, sonuc3 = st.columns(3)
            sonuc1.metric("Ortalama hub hızı", f"{sonuc['hesap']['Hub Rüzgar Hızı'].mean():.2f} m/s")
            sonuc2.metric("Ortalama tek türbin güç", f"{sonuc['hesap']['Tek Türbin Güç kW'].mean() / 1000:.2f} MW")
            sonuc3.metric("Kurulu güç", f"{sonuc['kurulu_guc_mw']:.1f} MW")

            sonuc4, sonuc5, sonuc6 = st.columns(3)
            sonuc4.metric("Geçerli kayıtlardan net enerji tahmini", f"{sonuc['net_mwh']:,.0f} MWh")
            if sonuc.get("annual_ok", False):
                sonuc5.metric("Yıllık Net Üretim · Ön tahmin", f"{sonuc['yillik_net_mwh']:,.0f} MWh/yıl")
                sonuc6.metric("Kapasite faktörü · Ön tahmin", f"%{sonuc['kapasite_faktoru']:.1f}")
            else:
                sonuc5.metric("Yıllık Net Üretim", "Hesaplanmadı")
                sonuc6.metric("Kapasite faktörü", "Hesaplanmadı")
                st.warning("Yıllık veri kapsamı yetersiz. Eksik dönemler kalan ölçümlerle yıllığa ölçeklenmez.")
            for _qad, _qstatus in sonuc.get("quality",{}).items():
                st.caption(f"{veri_seti_gorunur_adi(_qad)} · Geçerli ölçüm: %{_qstatus.get('coverage_pct',0):.2f} · En uzun boşluk: {_qstatus.get('longest_gap_hours',float('nan')):.1f} saat")

            if yerlesim_turbinleri:
                st.caption("Yerleşim bazında yıllık AEP bu sürümde gösterilmez. Ortalama saha hızını doğrudan güç eğrisine uygulamak, zaman serisi enerji hesabıyla eşdeğer değildir; GWA ve mekânsal dönüşüm ayrıca doğrulanmalıdır.")

        st.markdown("---")
        grafik1, grafik2 = st.columns(2)

        with grafik1:
            st.subheader("Türbin güç eğrisi")
            curve = model_bilgisi["power_curve"]
            curve_df = pd.DataFrame({
                "Rüzgar Hızı (m/s)": curve["wind_speed"],
                "Güç (kW)": curve["power_kw"]
            })
            curve_fig = px.line(
                curve_df,
                x="Rüzgar Hızı (m/s)",
                y="Güç (kW)",
                markers=True
            )
            curve_fig.update_layout(height=390, margin=dict(l=40, r=20, t=20, b=40))
            st.plotly_chart(curve_fig, use_container_width=True, config={"displaylogo": False})

        with grafik2:
            st.subheader("Aylık net enerji")
            aylik_enerji = sonuc["hesap"].copy()
            aylik_enerji["Ay"] = aylik_enerji["TIMESTAMP"].dt.to_period("M").astype(str)
            aylik_enerji = aylik_enerji.groupby("Ay", as_index=False)["Santral Net Enerji kWh"].sum()
            aylik_enerji["Net Enerji (MWh)"] = aylik_enerji["Santral Net Enerji kWh"] / 1000.0
            aylik_fig = px.bar(aylik_enerji, x="Ay", y="Net Enerji (MWh)")
            aylik_fig.update_layout(height=390, margin=dict(l=40, r=20, t=20, b=40))
            st.plotly_chart(aylik_fig, use_container_width=True, config={"displaylogo": False})

        with st.expander("Wake analizi ve hesaplama verileri"):
            if wake_tablo:
                st.subheader("Türbin bazlı ön wake analizi")
                guvenli_dataframe(pd.DataFrame(wake_tablo).round(2), use_container_width=True, hide_index=True)

            hub_basligi = f"Hub Rüzgâr Hızı ({hub_yuksekligi:g} m)"
            hesap_kolonlari = [
                "TIMESTAMP",
                "Hub Rüzgar Hızı",
                "Tek Türbin Güç kW",
                "Santral Brüt Güç kW",
                "Santral Net Güç kW",
                "Tek Türbin Enerji kWh",
                "Santral Brüt Enerji kWh",
                "Santral Net Enerji kWh",
            ]
            hesap_kolonlari = [k for k in hesap_kolonlari if k in sonuc["hesap"].columns]
            gosterilecek = sonuc["hesap"][hesap_kolonlari].copy().rename(columns={
                "Hub Rüzgar Hızı": hub_basligi
            })

            if st.checkbox("Hesaplama tablosunu ekranda göster", value=False, key="hesap_tablo_goster_hizli"):
                ekranda_gosterilecek = gosterilecek.head(1000)
                if len(gosterilecek) > 1000:
                    st.info(
                        f"{len(gosterilecek):,} kaydın ilk 1.000 adedi gösteriliyor. "
                        "Tam tabloyu aşağıdan indirebilirsiniz."
                    )
                guvenli_dataframe(
                    ekranda_gosterilecek,
                    use_container_width=True,
                    height=420,
                    hide_index=True
                )
            st.download_button(
                "Tam hesaplama verisini CSV olarak indir",
                data=gosterilecek.to_csv(index=False).encode("utf-8-sig"),
                file_name="uretim_hesaplama_verisi.csv",
                mime="text/csv",
                key="hesap_csv_v744"
            )


# Yalniz bu tarayici sekmesinin durumunu kaydet.
app_state["active_page"] = st.session_state.get("aktif_sayfa_v8", app_state.get("active_page", "Ana Sayfa"))
app_state["measurement_step"] = int(st.session_state.get("ruzgar_olcumleri_adim_v112", app_state.get("measurement_step", 1)) or 1)
kalici_durumu_kaydet(app_state)
