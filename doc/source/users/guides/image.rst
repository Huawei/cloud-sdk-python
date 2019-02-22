Using OpenStack Image
=====================

Before working with the Image service, you'll need to create a connection
to your OpenStack cloud by following the :doc:`connect` user guide. This will
provide you with the ``conn`` variable used in the examples below.

The primary resource of the Image service is the image.

List Images
-----------

An **image** is a collection of files for a specific operating system
that you use to create or rebuild a server. OpenStack provides
`pre-built images <http://docs.openstack.org/image-guide/obtain-images.html>`_.
You can also create custom images, or snapshots, from servers that you have
launched. Images come in different formats and are sometimes called virtual
machine images.

.. literalinclude:: ../examples/image/list.py
   :pyobject: list_images

Full example: `image resource list`_

Create Image
------------

Create an image by uploading its data and setting its attributes.

.. literalinclude:: ../examples/image/create.py
   :pyobject: upload_image

Full example: `image resource create`_

.. _download_image-stream-true:

Downloading an Image with stream=True
-------------------------------------

As images are often very large pieces of data, storing their entire contents
in the memory of your application can be less than desirable. A more
efficient method may be to iterate over a stream of the response data.

By choosing to stream the response content, you determine the ``chunk_size``
that is appropriate for your needs, meaning only that many bytes of data are
read for each iteration of the loop until all data has been consumed.
See :meth:`requests.Response.iter_content` for more information, as well
as Requests' :ref:`body-content-workflow`.

When you choose to stream an image download, openstacksdk is no longer
able to compute the checksum of the response data for you. This example
shows how you might do that yourself, in a very similar manner to how
the library calculates checksums for non-streamed responses.

.. literalinclude:: ../examples/image/download.py
   :pyobject: download_image_stream

Downloading an Image with stream=False
--------------------------------------

If you wish to download an image's contents all at once and to memory,
simply set ``stream=False``, which is the default.

.. literalinclude:: ../examples/image/download.py
   :pyobject: download_image

Full example: `image resource download`_

Delete Image
------------

Delete an image.

.. literalinclude:: ../examples/image/delete.py
   :pyobject: delete_image

Full example: `image resource delete`_

.. _image resource create: http://git.openstack.org/cgit/openstack/python-openstacksdk/tree/examples/image/create.py
.. _image resource delete: http://git.openstack.org/cgit/openstack/python-openstacksdk/tree/examples/image/delete.py
.. _image resource list: http://git.openstack.org/cgit/openstack/python-openstacksdk/tree/examples/image/list.py
.. _image resource download: http://git.openstack.org/cgit/openstack/python-openstacksdk/tree/examples/image/download.py
