// Copyright 2024 Advanced Micro Devices, Inc
//
// Licensed under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include "shortfin/local_device.h"

#include <fmt/core.h>
#include <fmt/ranges.h>

namespace shortfin {

// -------------------------------------------------------------------------- //
// LocalDeviceAddress
// -------------------------------------------------------------------------- //

LocalDeviceAddress::LocalDeviceAddress(
    std::string_view system_device_class, std::string_view logical_device_class,
    std::string_view hal_driver_prefix, iree_host_size_t instance_ordinal,
    iree_host_size_t queue_ordinal,
    std::vector<iree_host_size_t> instance_topology_address)
    : system_device_class(std::move(system_device_class)),
      logical_device_class(std::move(logical_device_class)),
      hal_driver_prefix(std::move(hal_driver_prefix)),
      instance_ordinal(instance_ordinal),
      queue_ordinal(queue_ordinal),
      instance_topology_address(instance_topology_address),
      device_name(
          fmt::format("{}:{}:{}@{}", this->system_device_class,
                      this->instance_ordinal, this->queue_ordinal,
                      fmt::join(this->instance_topology_address, ","))) {}

// -------------------------------------------------------------------------- //
// LocalDevice
// -------------------------------------------------------------------------- //

LocalDevice::LocalDevice(LocalDeviceAddress address,
                         iree_hal_device_ptr hal_device, int node_affinity,
                         bool node_locked)
    : address_(std::move(address)),
      hal_device_(std::move(hal_device)),
      node_affinity_(node_affinity),
      node_locked_(node_locked) {}

LocalDevice::~LocalDevice() = default;

}  // namespace shortfin
