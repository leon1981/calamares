#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# === This file is part of Calamares - <http://github.com/calamares> ===
#
# Copyright 2014-2016, Anke Boersma <demm@kaosx.us>
#
# Calamares is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Calamares is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import libcalamares
import os


def modify_grub_default(partitions, root_mount_point, distributor):

    default_dir = os.path.join(root_mount_point, "etc/default")
    default_grub = os.path.join(default_dir, "grub")
    swap_uuid = ""

    if not os.path.exists(default_dir):
        return ("Directory does not exist", "The directory {} does not exist on "
        "the target".format(default_dir))

    cryptdevice_params = []
    
    # GRUB needs to decrypt the partition that /boot is on, which may be / or /boot
    boot_mountpoint = "/"
    for partition in partitions:
        if partition["mountPoint"] == "/boot":
            boot_mountpoint = "/boot"

    for partition in partitions:
        if partition["fs"] == "linuxswap":
            swap_uuid = partition["uuid"]

        if partition["mountPoint"] == boot_mountpoint and "luksMapperName" in partition:
            cryptdevice_params = [
                "cryptdevice=UUID={!s}:{!s}".format(partition["luksUuid"],
                                                    partition["luksMapperName"]),
                "root=/dev/mapper/{!s}".format(partition["luksMapperName"])
            ]

    if swap_uuid != "":
        kernel_cmd = 'GRUB_CMDLINE_LINUX_DEFAULT="resume=UUID={!s} quiet systemd.show_status=0 {!s}"'.format(
            swap_uuid, " ".join(cryptdevice_params))
    else:
        kernel_cmd = 'GRUB_CMDLINE_LINUX_DEFAULT="quiet systemd.show_status=0 {!s}"'.format(" ".join(cryptdevice_params))

    if not os.path.exists(default_dir):
        os.mkdir(default_dir)

    with open(default_grub, 'r') as grub_file:
        lines = [x.strip() for x in grub_file.readlines()]

    for i in range(len(lines)):
        if lines[i].startswith("#GRUB_CMDLINE_LINUX_DEFAULT"):
            lines[i] = kernel_cmd
        elif lines[i].startswith("GRUB_CMDLINE_LINUX_DEFAULT"):
            lines[i] = kernel_cmd
        elif lines[i].startswith("#GRUB_DISTRIBUTOR") or lines[i].startswith("GRUB_DISTRIBUTOR"):
            lines[i] = "GRUB_DISTRIBUTOR=\"{!s}\"".format(distributor)

    if cryptdevice_params:
        lines.append("GRUB_ENABLE_CRYPTODISK=y")

    with open(default_grub, 'w') as grub_file:
        grub_file.write("\n".join(lines) + "\n")

    return None


def run():

    fw_type = libcalamares.globalstorage.value("firmwareType")
    
    if libcalamares.globalstorage.value("bootLoader") is None:
        return None
    
    if fw_type == 'efi':
        print('EFI system')
        return None

    partitions = libcalamares.globalstorage.value("partitions")
    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
    distributor = libcalamares.job.configuration["distributor"]
    return modify_grub_default(partitions, root_mount_point, distributor)
