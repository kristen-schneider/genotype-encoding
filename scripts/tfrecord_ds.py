import basic_ds

import tensorflow as tf
from itertools import zip_longest, takewhile
import numpy as np
import functools

class DataWriter:
    def __init__(self, sample_ID_file, sample_encoding_file, pairwise_IBD_file, out_dir):
        self.sample_ID_file = sample_ID_file
        self.sample_encoding_file = sample_encoding_file
        self.pairwise_IBD_file = pairwise_IBD_file
        self.out_dir = out_dir

    # @staticmethod
    # def get_basic_dataset(input_file):
    #     """
    #     Builds a tensorflow dataset object from file with 3 columns:
    #     sample1, sample2, IBD_distance
    #     :param CNN_input_file:
    #     :return: tensorflow dataset object for input to cnn model
    #     """
    #     f = open(input_file, 'r')
    #     header = f.readline()
    #     sample1_data, sample2_data, distances_data = [], [], []
    #     for line in f:
    #         currS1, currS2 = [], []
    #         A = line.strip().split()
    #
    #         # for i in A[0]: currS1.append(int(i))
    #         # sample1_data.append(currS1)
    #         #
    #         # for j in A[1]: currS2.append(int(j))
    #         # sample2_data.append(currS1)
    #         sample1_data.append(A[0])
    #         sample2_data.append(A[1])
    #         distances_data.append(A[2])
    #
    #     # each set of input data is its own tensor
    #     sample1_ds = tf.data.Dataset.from_tensor_slices(sample1_data)
    #     sample2_ds = tf.data.Dataset.from_tensor_slices(sample2_data)
    #     distances_ds = tf.data.Dataset.from_tensor_slices(distances_data)
    #
    #     # map sample encodings to list of ints and distance values to float
    #     # sample1_int = sample1_ds.map(lambda x: int(x))
    #     # sample2_int = sample2_ds.map(lambda x: int(x))
    #     distances_float = distances_ds.map(lambda x: float(x))
    #
    #     # zip 3 tensor items together into one dataset
    #     full_ds = tf.data.Dataset.zip((sample1_ds, sample2_ds, distances_float))
    #     # puts (__) element into a batch
    #     # full_ds_batch = full_ds.batch(2)
    #     return full_ds
    def _sample_encoding_dict(self):
        f_IDs = open(self.sample_ID_file, 'r')
        f_encodings = open(self.)

    @staticmethod
    def _grouper(iterable, n, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks,
        Taken from python itertools docs
        """
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    @staticmethod
    def _bytes_feature(value):
        """

        :param value: bytes
        :return: takes input value and serializes
        """
        if isinstance(value, tf.Tensor):
            value = value.numpy()
        elif not isinstance(value, bytes):
            value = value.encode()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _int64_feature(value):
        """
        :param value: integer
        :return: takes input integer value and serializes
        """
        if not isinstance(value, list):
            value = [value]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    @staticmethod
    def _float_feature(value):
        """
        :param value: float
        :return: takes input float value and serializes
        """
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    @staticmethod
    def _serialize_example(sample1, sample2, distance):
        """
        given an input tensor (s1, s2, distance), serialize the entire input
        """
        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    'sample1': DataWriter._bytes_feature(sample1),
                    'sample2': DataWriter._bytes_feature(sample2),
                    'distance': DataWriter._float_feature(distance),
                }
            )
        )
        return example.SerializeToString()

    @staticmethod
    def _write_batch(out_dir, batch_index, basicDS):
        """
        Write a single batch of images to TFRecord format
        """
        with tf.io.TFRecordWriter(
                f"{out_dir}/_{batch_index:05d}.tfrec") as writer:
            for s1, s2, d in basicDS:
                serialized_example = DataWriter._serialize_example(s1, s2, d)
                writer.write(serialized_example)

    def to_tfrecords(self):
        """
        1. Read data into memory
        2.
        """
        num_records = 100
        for i in range(num_records):
        self._write_batch(self.out_dir, 1)



# class DataReader:
#     def __init__(self,
#                  data_list,  # list of original images in the dataset
#                  tfrec_list,  # list of tfrecords in the dataset (s3 or local)
#                  num_processes,
#                  batch_size):
#         self.data_list = data_list
#         self.tfrec_list = tfrec_list
#         self.num_processes = num_processes
#         self.batch_size = batch_size
#
#     @staticmethod
#     def _parse_serialized_example(serialized_example):
#         """
#         Given a serialized example with the below format, extract/deserialize
#         the image and (one-hot) label
#         """
#         features = {
#             'filename': tf.io.FixedLenFeature((), tf.string),
#             'image': tf.io.FixedLenFeature((), tf.string),
#             'label': tf.io.FixedLenFeature((), tf.int64)
#         }
#         example = tf.io.parse_single_example(serialized_example, features)
#
#         # read image and perform transormations
#         image = DataReader._parse_image(example['image'])
#         image = tf.image.per_image_standardization(image)
#
#         label = example['label']
#         return image, tf.one_hot(label, depth=3, dtype=tf.int64)
#
#     def get_dataset(self):
#         n_images = len(open(self.data_list).readlines())
#
#         # we don't need examples to be loaded in order (better speed)
#         options = tf.data.Options()
#         options.experimental_deterministic = False
#
#         with open(self.tfrec_list) as f:
#             files = [filename.rstrip() for filename in f]
#             dataset = tf.data.Dataset.from_tensor_slices(files) \
#                 .shuffle(len(files)) \
#                 .with_options(options)
#
#         dataset = tf.dataset.interleave(
#             tf.data.TFRecordDataset,
#             cycle_length=self.num_processes,
#             num_parallel_calls=self.num_processes) \
#  \
#                 dataset = tf.dataset.map(
#                     functools.partial(DataReader._parse_serialized_example),
#                     num_parallel_calls=self.num_processes) \
#                     .repeat() \
#                     .shuffle(buffer_size=1000) \
#                     .batch(self.batch_size, drop_remainder=False) \
#                     .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
#
#         return dataset, n_images