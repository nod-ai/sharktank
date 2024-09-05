# Copyright 2024 Advanced Micro Devices, Inc
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import unittest
from typing import List

import torch
from shark_turbine.aot import *
from sharktank.models.llama.testing import make_moe_block_theta, make_rand_torch
from sharktank.layers.mixture_of_experts_block import SparseMoeBlock
from sharktank import ops


class SparseMoeBlockTest(unittest.TestCase):
    def test(self):
        model = SparseMoeBlock(
            theta=make_moe_block_theta()("blk.0"),
            expert_count=8,
            expert_used_count=2,
            rms_epsilon=1e-5,
        )
        fxb = FxProgramsBuilder(model)
        input = make_rand_torch((2, 16, 6144))

        @fxb.export_program(name="moe_block", args=(input,))
        def _(model, input: torch.Tensor) -> torch.Tensor:
            return model(input)


if __name__ == "__main__":
    unittest.main()