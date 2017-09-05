import sys
import tensorflow as tf
from datetime import datetime

device_name = sys.argv[1]  # Choose device from cmd line. Options: gpu or cpu
shape = (int(sys.argv[2]), int(sys.argv[2]))
repeats = int(sys.argv[3])
if device_name == "gpu":
    device_name = "/gpu:0"
else:
    device_name = "/cpu:0"

with tf.device(device_name):
    x = tf.random_uniform(shape=shape, minval=0, maxval=1)
    y = x
    for i in range(repeats):
        y = tf.matmul(y, x) / tf.reduce_sum(y)
    sum_operation = tf.reduce_sum(y)


start_time = datetime.now()
with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as session:
        result = session.run(sum_operation)
        # print(result)
end_time = datetime.now()
print("\n\nShape:{} Device:{} Repeats:{}".format(shape, device_name, repeats))
print(end_time - start_time)
