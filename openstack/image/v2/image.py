# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
#      Huawei has modified this source file.
#     
#         Copyright 2018 Huawei Technologies Co., Ltd.
#         
#         Licensed under the Apache License, Version 2.0 (the "License"); you may not
#         use this file except in compliance with the License. You may obtain a copy of
#         the License at
#         
#             http://www.apache.org/licenses/LICENSE-2.0
#         
#         Unless required by applicable law or agreed to in writing, software
#         distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#         WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#         License for the specific language governing permissions and limitations under
#         the License.

import hashlib
import logging

from openstack import exceptions
from openstack.image import image_service
from openstack import resource2
from openstack import utils

_logger = logging.getLogger(__name__)


class Image(resource2.Resource):
    resources_key = 'images'
    base_path = '/images'
    service = image_service.ImageService()

    # capabilities
    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True
    patch_update = True

    _query_mapping = resource2.QueryParameters("name", "visibility",
                                               "member_status", "owner",
                                               "status", "size_min",
                                               "size_max", "sort_key",
                                               "sort_dir", "sort", "tag",
                                               "created_at", "updated_at",
                                               "__platform", "__imagetype",
                                               "__os_version", "__isregistered",
                                               "protected", "id", "container_format",
                                               "disk_format", "min_ram", "min_disk",
                                               "__os_bit", "__os_type",
                                               "__support_kvm", "__support_xen",
                                               "__support_diskintensive",
                                               "__support_highperformance",
                                               "__support_xen_gpu_type")

    # NOTE: Do not add "self" support here. If you've used Python before,
    # you know that self, while not being a reserved word, has special
    # meaning. You can't call a class initializer with the self name
    # as the first argument and then additionally in kwargs, as we
    # do when we're constructing instances from the JSON body.
    # Resource.list explicitly pops off any "self" keys from bodies so
    # that we don't end up getting the following:
    # TypeError: __init__() got multiple values for argument 'self'

    # The image data (bytes or a file-like object)
    data = None
    # Properties
    #: Hash of the image data used. The Image service uses this value
    #: for verification.
    checksum = resource2.Body('checksum')
    #: The container format refers to whether the VM image is in a file
    #: format that also contains metadata about the actual VM.
    #: Container formats include OVF and Amazon AMI. In addition,
    #: a VM image might not have a container format - instead,
    #: the image is just a blob of unstructured data.
    container_format = resource2.Body('container_format')
    #: The date and time when the image was created.
    created_at = resource2.Body('created_at')
    #: Valid values are: aki, ari, ami, raw, iso, vhd, vdi, qcow2, or vmdk.
    #: The disk format of a VM image is the format of the underlying
    #: disk image. Virtual appliance vendors have different formats
    #: for laying out the information contained in a VM disk image.
    disk_format = resource2.Body('disk_format')
    #: Defines whether the image can be deleted.
    #: *Type: bool*
    is_protected = resource2.Body('protected', type=bool)
    #: The minimum disk size in GB that is required to boot the image.
    min_disk = resource2.Body('min_disk')
    #: The minimum amount of RAM in MB that is required to boot the image.
    min_ram = resource2.Body('min_ram')
    #: The name of the image.
    name = resource2.Body('name')
    #: The ID of the owner, or project, of the image.
    owner_id = resource2.Body('owner')
    #: Properties, if any, that are associated with the image.
    properties = resource2.Body('properties', type=dict)
    #: The size of the image data, in bytes.
    size = resource2.Body('size', type=int)
    #: When present, Glance will attempt to store the disk image data in the
    #: backing store indicated by the value of the header. When not present,
    #: Glance will store the disk image data in the backing store that is
    #: marked default. Valid values are: file, s3, rbd, swift, cinder,
    #: gridfs, sheepdog, or vsphere.
    store = resource2.Body('store')
    #: The image status.
    status = resource2.Body('status')
    #: Tags, if any, that are associated with the image.
    tags = resource2.Body('tags')
    #: The date and time when the image was updated.
    updated_at = resource2.Body('updated_at')
    #: The virtual size of the image.
    virtual_size = resource2.Body('virtual_size')
    #: The image visibility.
    visibility = resource2.Body('visibility')
    #: The URL for the virtual machine image file.
    file = resource2.Body('file')
    #: A list of URLs to access the image file in external store.
    #: This list appears if the show_multiple_locations option is set
    #: to true in the Image service's configuration file.
    locations = resource2.Body('locations')
    #: The URL to access the image file kept in external store. It appears
    #: when you set the show_image_direct_url option to true in the
    #: Image service's configuration file.
    direct_url = resource2.Body('direct_url')
    #: An image property.
    path = resource2.Body('path')
    #: Value of image property used in add or replace operations expressed
    #: in JSON notation. For example, you must enclose strings in quotation
    #: marks, and you do not enclose numeric values in quotation marks.
    value = resource2.Body('value')
    #: The URL to access the image file kept in external store.
    url = resource2.Body('url')
    #: The location metadata.
    metadata = resource2.Body('metadata', type=dict)

    # Additional Image Properties
    # http://docs.openstack.org/developer/glance/common-image-properties.html
    # http://docs.openstack.org/cli-reference/glance-property-keys.html
    #: The CPU architecture that must be supported by the hypervisor.
    architecture = resource2.Body("architecture")
    #: The hypervisor type. Note that qemu is used for both QEMU and
    #: KVM hypervisor types.
    hypervisor_type = resource2.Body("hypervisor-type")
    #: Optional property allows created servers to have a different bandwidth
    #: cap than that defined in the network they are attached to.
    instance_type_rxtx_factor = resource2.Body("instance_type_rxtx_factor",
                                               type=float)
    # For snapshot images, this is the UUID of the server used to
    #: create this image.
    instance_uuid = resource2.Body('instance_uuid')
    #: Specifies whether the image needs a config drive.
    #: `mandatory` or `optional` (default if property is not used).
    needs_config_drive = resource2.Body('img_config_drive')
    #: The ID of an image stored in the Image service that should be used
    #: as the kernel when booting an AMI-style image.
    kernel_id = resource2.Body('kernel_id')
    #: The common name of the operating system distribution in lowercase
    os_distro = resource2.Body('os_distro')
    #: The operating system version as specified by the distributor.
    os_version = resource2.Body('__os_version')
    #: Secure Boot is a security standard. When the instance starts,
    #: Secure Boot first examines software such as firmware and OS by
    #: their signature and only allows them to run if the signatures are valid.
    needs_secure_boot = resource2.Body('os_secure_boot')
    #: The ID of image stored in the Image service that should be used as
    #: the ramdisk when booting an AMI-style image.
    ramdisk_id = resource2.Body('ramdisk_id')
    #: The virtual machine mode. This represents the host/guest ABI
    #: (application binary interface) used for the virtual machine.
    vm_mode = resource2.Body('vm_mode')
    #: The preferred number of sockets to expose to the guest.
    hw_cpu_sockets = resource2.Body('hw_cpu_sockets', type=int)
    #: The preferred number of cores to expose to the guest.
    hw_cpu_cores = resource2.Body('hw_cpu_cores', type=int)
    #: The preferred number of threads to expose to the guest.
    hw_cpu_threads = resource2.Body('hw_cpu_threads', type=int)
    #: Specifies the type of disk controller to attach disk devices to.
    #: One of scsi, virtio, uml, xen, ide, or usb.
    hw_disk_bus = resource2.Body('hw_disk_bus')
    #: Adds a random-number generator device to the image's instances.
    hw_rng_model = resource2.Body('hw_rng_model')
    #: For libvirt: Enables booting an ARM system using the specified
    #: machine type.
    #: For Hyper-V: Specifies whether the Hyper-V instance will be a
    #: generation 1 or generation 2 VM.
    hw_machine_type = resource2.Body('hw_machine_type')
    #: Enables the use of VirtIO SCSI (virtio-scsi) to provide block device
    #: access for compute instances; by default, instances use VirtIO Block
    #: (virtio-blk).
    hw_scsi_model = resource2.Body('hw_scsi_model')
    #: Specifies the count of serial ports that should be provided.
    hw_serial_port_count = resource2.Body('hw_serial_port_count', type=int)
    #: The video image driver used.
    hw_video_model = resource2.Body('hw_video_model')
    #: Maximum RAM for the video image.
    hw_video_ram = resource2.Body('hw_video_ram', type=int)
    #: Enables a virtual hardware watchdog device that carries out the
    #: specified action if the server hangs.
    hw_watchdog_action = resource2.Body('hw_watchdog_action')
    #: The kernel command line to be used by the libvirt driver, instead
    #: of the default.
    os_command_line = resource2.Body('os_command_line')
    #: Specifies the model of virtual network interface device to use.
    hw_vif_model = resource2.Body('hw_vif_model')
    #: If true, this enables the virtio-net multiqueue feature.
    #: In this case, the driver sets the number of queues equal to the
    #: number of guest vCPUs. This makes the network performance scale
    #: across a number of vCPUs.
    is_hw_vif_multiqueue_enabled = resource2.Body('hw_vif_multiqueue_enabled',
                                                  type=bool)
    #: If true, enables the BIOS bootmenu.
    is_hw_boot_menu_enabled = resource2.Body('hw_boot_menu', type=bool)
    #: The virtual SCSI or IDE controller used by the hypervisor.
    vmware_adaptertype = resource2.Body('vmware_adaptertype')
    #: A VMware GuestID which describes the operating system installed
    #: in the image.
    vmware_ostype = resource2.Body('vmware_ostype')
    #: If true, the root partition on the disk is automatically resized
    #: before the instance boots.
    has_auto_disk_config = resource2.Body('auto_disk_config', type=bool)
    #: The operating system installed on the image.
    os_type = resource2.Body('__os_type')
    #: The image type.
    imagetype = resource2.Body("__imagetype")
    #: The bit of the operation system installed on the image.
    os_bit = resource2.Body("__os_bit")
    #: The platform of the operation system installed on the image.
    platform = resource2.Body("__platform")
    #: Whether it is a registered image.
    isregistered = resource2.Body("__isregistered")
    #: Tag.
    tag = resource2.Body("tag")
    #: Status of member.
    member_status = resource2.Body("member_status")
    #: Whether to support kvm.
    support_kvm = resource2.Body("__support_kvm")
    #: Whether to support xen.
    support_xen = resource2.Body("__support_xen")
    #: Whether to support dense storage.
    support_diskintensive = resource2.Body("__support_diskintensive")
    #: Whether to support high computing performance.
    support_highperformance = resource2.Body("__support_highperformance")
    #: Whether to support the GPU optimization type under the XEN virtualization platform.
    support_xen_gpu_type = resource2.Body("__support_xen_gpu_type")
    #: Indicates that the current mirror source is imported from outside.
    root_origin = resource2.Body("__root_origin")
    #: Indicates the location of the system disk slot where the current image
    #: corresponds to the cloud server.
    sequence_num = resource2.Body("__sequence_num")
    #: Image link's infomation.
    self_info = resource2.Body("self")
    #: View image.
    schema = resource2.Body("schema")
    #: Whether it is a deleted image.
    deleted = resource2.Body("deleted", type=bool)
    #: Description of image.
    description = resource2.Body("__description")
    #: Mirror usage environment type
    virtual_env_type = resource2.Body("virtual_env_type")
    #: Mirror backend storage type.
    image_source_type = resource2.Body("__image_source_type")
    #: Delete time.
    deleted_at = resource2.Body("deleted_at")
    #: Parent image ID.
    originalimagename = resource2.Body("__originalimagename")
    #: Id of backup.
    backup_id = resource2.Body("__backup_id")
    #: The product ID of the market image.
    productcode = resource2.Body("__productcode")
    #: Size of image.
    image_size = resource2.Body("__image_size")
    #: Mirror source.
    data_origin = resource2.Body("__data_origin")
    #: Update time.
    update_at = resource2.Body("update_at")
    # Create time
    create_at = resource2.Body("create_at")
    #: The storage location of the image.
    image_location = resource2.Body("__image_location")
    #: Indicates the enterprise project to which the current image belongs.
    enterprise_project_id = resource2.Body("enterprise_project_id")
    #: The maximum memory supported by the image.
    max_ram = resource2.Body("max_ram")


    def _action(self, session, action):
        """Call an action on an image ID."""
        url = utils.urljoin(self.base_path, self.id, 'actions', action)
        endpoint_override = self.service.get_endpoint_override()
        return session.post(url, endpoint_filter=self.service, endpoint_override = endpoint_override)

    def deactivate(self, session):
        """Deactivate an image

        Note: Only administrative users can view image locations
        for deactivated images.
        """
        self._action(session, "deactivate")

    def reactivate(self, session):
        """Reactivate an image

        Note: The image must exist in order to be reactivated.
        """
        self._action(session, "reactivate")

    def add_tag(self, session, tag):
        """Add a tag to an image"""
        url = utils.urljoin(self.base_path, self.id, 'tags', tag)
        endpoint_override = self.service.get_endpoint_override()
        session.put(url, endpoint_filter=self.service, endpoint_override = endpoint_override)

    def remove_tag(self, session, tag):
        """Remove a tag from an image"""
        url = utils.urljoin(self.base_path, self.id, 'tags', tag)
        endpoint_override = self.service.get_endpoint_override()
        session.delete(url, endpoint_filter=self.service, endpoint_override = endpoint_override)

    def upload(self, session):
        """Upload data into an existing image"""
        url = utils.urljoin(self.base_path, self.id, 'file')
        endpoint_override = self.service.get_endpoint_override()
        session.put(url, endpoint_filter=self.service, data=self.data,
                    headers={"Content-Type": "application/octet-stream",
                             "Accept": ""},
                    endpoint_override = endpoint_override)

    def download(self, session, stream=False):
        """Download the data contained in an image"""
        # TODO(briancurtin): This method should probably offload the get
        # operation into another thread or something of that nature.
        url = utils.urljoin(self.base_path, self.id, 'file')
        endpoint_override = self.service.get_endpoint_override()
        resp = session.get(url, endpoint_filter=self.service, stream=stream,
                           endpoint_override = endpoint_override)

        # See the following bug report for details on why the checksum
        # code may sometimes depend on a second GET call.
        # https://bugs.launchpad.net/python-openstacksdk/+bug/1619675
        checksum = resp.headers.get("Content-MD5")

        if checksum is None:
            # If we don't receive the Content-MD5 header with the download,
            # make an additional call to get the image details and look at
            # the checksum attribute.
            details = self.get(session)
            checksum = details.checksum

        # if we are returning the repsonse object, ensure that it
        # has the content-md5 header so that the caller doesn't
        # need to jump through the same hoops through which we
        # just jumped.
        if stream:
            resp.headers['content-md5'] = checksum
            return resp

        if checksum is not None:
            digest = hashlib.md5(resp.content).hexdigest()
            if digest != checksum:
                raise exceptions.InvalidResponse(
                    "checksum mismatch: %s != %s" % (checksum, digest))
        else:
            _logger.warn(
                "Unable to verify the integrity of image %s" % (self.id))

        return resp.content

    def update(self, session, **attrs):
        url = utils.urljoin(self.base_path, self.id)
        headers = {
            'Content-Type': 'application/openstack-images-v2.1-json-patch',
            'Accept': ''
        }
        patch_body = [attrs]
        endpoint_override = self.service.get_endpoint_override()
        resp = session.patch(url, endpoint_filter=self.service,
                             json=patch_body,
                             headers=headers,
                             endpoint_override=endpoint_override)
        self._translate_response(resp, has_body=True)
        return self
