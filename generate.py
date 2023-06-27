#!/usr/bin/env python3
import os
import shutil
import subprocess
import zipfile
from io import BytesIO

import requests

releases = [
    '2023.1',
    '2022.3',
    '2022.2',
    '2022.1',
    '2021.4',
    '2021.3',
    '2021.2',
    '2021.1',
    '2020.4',
    '2020.3',
    '2020.2',
    '2020.1',
    '2019.4',
    '2019.3',
    '2019.2',
    '2019.1',
    '2018.3',
    '2018.2',
    '2018.1',
    '2017.3',
#    '2017.2',  Doesn't exist??
    '2017.1',
    '2016.3',
    '2016.2',
    '2016.1',
    '1.0.0',
]


VERSION = "DSP8010_{}"

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
subprocess.run(["git", "init"])

for version in reversed(releases):
    dsp_version = VERSION.format(version)
    r = requests.get(
        "https://www.dmtf.org/sites/default/files/standards/documents/"
        + dsp_version
        + ".zip",
    )

    r.raise_for_status()

    zipBytesIO = BytesIO(r.content)
    zip_ref = zipfile.ZipFile(zipBytesIO)

    zip_ref.extractall()

    try:
        shutil.rmtree("__MACOSX")
    except FileNotFoundError:
        pass

    try:
        shutil.copytree(dsp_version, SCRIPT_DIR, dirs_exist_ok=True)
        shutil.rmtree(dsp_version)
    except FileNotFoundError:
        pass

    try:
        shutil.move(dsp_version + ".pdf", "DSP8010.pdf")
    except FileNotFoundError:
        pass

    try:
        shutil.move("README8010.pdf", "DSP8010.pdf")
    except FileNotFoundError:
        pass

    try:
        shutil.move("README8010.htm", "DSP8010.html")
    except FileNotFoundError:
        pass

    try:
        shutil.move("README8010.html", "DSP8010.html")
    except FileNotFoundError:
        pass

    try:
        shutil.move(dsp_version + ".html", "DSP8010.html")
    except FileNotFoundError:
        pass
    try:
        shutil.move(dsp_version + ".htm", "DSP8010.html")
    except FileNotFoundError:
        pass
    if os.path.exists("metadata"):
        try:
            shutil.rmtree("csdl")
        except FileNotFoundError:
            pass
        os.rename("metadata", "csdl")

    try:
        os.remove("Redfish 2017 Release 1 Overview.pptx")
    except FileNotFoundError:
        pass

    try:
        os.remove(".DS_Store")
    except FileNotFoundError:
        pass

    if not os.path.exists('registries'):
        os.makedirs('registries')

    if version not in ["2016.1", "2016.2", "2016.3", "2017.1", "2017.3", "2018.3"]:
        dsp_version = "DSP8011_{}".format(version)
        r = requests.get(
            "https://www.dmtf.org/sites/default/files/standards/documents/"
            + dsp_version
            + ".zip",
        )
        r.raise_for_status()

        zipBytesIO = BytesIO(r.content)
        zip_ref = zipfile.ZipFile(zipBytesIO)

        zip_ref.extractall(path='registries')

    try:
        shutil.rmtree("registries/__MACOSX")
    except FileNotFoundError:
        pass

    try:
        shutil.copytree("registries/DSP8011_{}".format(version), "registries/", dirs_exist_ok=True)
        shutil.rmtree("registries/" + dsp_version)
    except FileNotFoundError:
        pass

    try:
        shutil.copytree("registries/ZIP-Bundle", "registries/", dirs_exist_ok=True)
        shutil.rmtree("registries/ZIP-Bundle")
    except FileNotFoundError:
        pass

    try:
        shutil.move("registries/DSP8011_{}.pdf".format(version), "registries/DSP8011.pdf")
    except FileNotFoundError:
        pass
    try:
        shutil.move("registries/DSP8011_{}.html".format(version), "registries/DSP8011.html")
    except FileNotFoundError:
        pass
    try:
        shutil.move("registries/DSP8011_{}.htm".format(version), "registries/DSP8011.html")
    except FileNotFoundError:
        pass
    try:
        shutil.move("registries/DSP8011_2019.1.pdf".format(version), "registries/DSP8011.pdf")
    except FileNotFoundError:
        pass
    try:
        shutil.move("registries/DSP8011_2019.1.html".format(version), "registries/DSP8011.html")
    except FileNotFoundError:
        pass



    subprocess.run(["git", "add", "*"])
    subprocess.run(["git", "add", "-u"])
    subprocess.run(["git", "commit", "-s", "-m", "Update to schema pack {}".format(version)])
    subprocess.run(["git", "tag", "-a", version, '-m', "Schema pack {}".format(version)])

