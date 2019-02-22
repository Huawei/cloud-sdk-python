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

from openstack.block_store.v2 import snapshot as _snapshot
from openstack.block_store.v2 import type as _type
from openstack.block_store.v2 import volume as _volume
from openstack import proxy2


class Proxy(proxy2.BaseProxy):

    def get_snapshot(self, snapshot):
        """Get a single snapshot

        :param snapshot: The value can be the ID of a snapshot or a
                         :class:`~openstack.volume.v2.snapshot.Snapshot`
                         instance.

        :returns: One :class:`~openstack.volume.v2.snapshot.Snapshot`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_snapshot.Snapshot, snapshot)

    def snapshots(self, details=True, **query):
        """Retrieve a generator of snapshots

        :param bool details: When set to ``False``
                    :class:`~openstack.block_store.v2.snapshot.Snapshot`
                    objects will be returned. The default, ``True``, will cause
                    :class:`~openstack.block_store.v2.snapshot.SnapshotDetail`
                    objects to be returned.
        :param kwargs \*\*query: Optional query parameters to be sent to limit
            the snapshots being returned.  Available parameters include:

            * name: Name of the snapshot as a string.
            * all_tenants: Whether return the snapshots of all tenants.
            * volume_id: volume id of a snapshot.
            * status: Value of the status of the snapshot so that you can
                      filter on "available" for example.

        :returns: A generator of snapshot objects.
        """
        snapshot = _snapshot.SnapshotDetail if details else _snapshot.Snapshot
        return self._list(snapshot, paginated=True, **query)

    def create_snapshot(self, **attrs):
        """Create a new snapshot from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.volume.v2.snapshot.Snapshot`,
                           comprised of the properties on the Snapshot class.

        :returns: The results of snapshot creation
        :rtype: :class:`~openstack.volume.v2.snapshot.Snapshot`
        """
        return self._create(_snapshot.Snapshot, **attrs)

    def delete_snapshot(self, snapshot, ignore_missing=True):
        """Delete a snapshot

        :param snapshot: The value can be either the ID of a snapshot or a
                         :class:`~openstack.volume.v2.snapshot.Snapshot`
                         instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the snapshot does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent snapshot.

        :returns: ``None``
        """
        self._delete(_snapshot.Snapshot, snapshot,
                     ignore_missing=ignore_missing)

    def get_type(self, type):
        """Get a single type

        :param type: The value can be the ID of a type or a
                     :class:`~openstack.volume.v2.type.Type` instance.

        :returns: One :class:`~openstack.volume.v2.type.Type`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_type.Type, type)

    def types(self):
        """Retrieve a generator of volume types

        :returns: A generator of volume type objects.
        """
        return self._list(_type.Type, paginated=False)

    def create_type(self, **attrs):
        """Create a new type from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.volume.v2.type.Type`,
                           comprised of the properties on the Type class.

        :returns: The results of type creation
        :rtype: :class:`~openstack.volume.v2.type.Type`
        """
        return self._create(_type.Type, **attrs)

    def delete_type(self, type, ignore_missing=True):
        """Delete a type

        :param type: The value can be either the ID of a type or a
                     :class:`~openstack.volume.v2.type.Type` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the type does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent type.

        :returns: ``None``
        """
        self._delete(_type.Type, type, ignore_missing=ignore_missing)

    def get_volume(self, volume):
        """Get a single volume

        :param volume: The value can be the ID of a volume or a
                       :class:`~openstack.volume.v2.volume.Volume` instance.

        :returns: One :class:`~openstack.volume.v2.volume.Volume`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_volume.Volume, volume)

    def volumes(self, details=True, sort_dir="desc", **query):
        """Retrieve a generator of volumes

        :param bool details: When set to ``False``
                    :class:`~openstack.block_store.v2.volume.Volume` objects
                    will be returned. The default, ``True``, will cause
                    :class:`~openstack.block_store.v2.volume.VolumeDetail`
                    objects to be returned.
        :param kwargs \*\*query: Optional query parameters to be sent to limit
            the volumes being returned.  Available parameters include:

            * name: Name of the volume as a string.
            * all_tenants: Whether return the volumes of all tenants
            * status: Value of the status of the volume so that you can filter
                    on "available" for example.

        :returns: A generator of volume objects.
        """
        volume = _volume.VolumeDetail if details else _volume.Volume
        query["sort_dir"] = sort_dir
        return self._list(volume, paginated=True, **query)

    def create_volume(self, **attrs):
        """Create a new volume from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.volume.v2.volume.Volume`,
                           comprised of the properties on the Volume class.

        :returns: The results of volume creation
        :rtype: :class:`~openstack.volume.v2.volume.Volume`
        """
        return self._create(_volume.Volume, **attrs)

    def delete_volume(self, volume, ignore_missing=True, cascade=False):
        """Delete a volume

        :param volume: The value can be either the ID of a volume or a
                       :class:`~openstack.volume.v2.volume.Volume` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the volume does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent volume.
        :param bool cascade: When set to ``Ture``
                    Delete all snapshots associated with the cloud drive.
                    The default value is false..

        :returns: ``None``
        """
        self._delete(_volume.Volume, volume, params={"cascade": cascade}, ignore_missing=ignore_missing)
