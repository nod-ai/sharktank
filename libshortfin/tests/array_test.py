# Copyright 2024 Advanced Micro Devices, Inc
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest

from _shortfin import lib as sfl


@pytest.fixture
def lsys():
    sc = sfl.host.CPUSystemBuilder()
    return sc.create_local_system()


@pytest.fixture
def scope(lsys):
    return lsys.create_scope()


def test_storage(scope):
    storage = sfl.array.storage.allocate_device(scope.device(0), 32)
    print(storage)
    ary = sfl.array.device_array(storage, [2, 4], sfl.array.float32)
    print(ary)
    print(ary.shape)
    assert ary.shape == [2, 4]
    assert ary.dtype == sfl.array.float32
    assert ary.device == scope.device(0)


def test_device_array(scope):
    ary1 = sfl.array.device_array(scope.device(0), [32, 1, 4], sfl.array.float32)
    print(ary1)
    assert ary1.shape == [32, 1, 4]
    assert ary1.dtype == sfl.array.float32
    assert scope.device(0) == ary1.device
