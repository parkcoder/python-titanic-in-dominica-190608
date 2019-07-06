import tensorflow as tf
from flask_restful import reqparse
import numpy as np

class CabbageController:
    def __init__(self):
        pass

    def service(self):
        pass

        X = tf.placeholder(tf.float32, shape=[None, 4])
        Y = tf.placeholder(tf.float32, shape=[None, 1])
        W = tf.Variable(tf.random_normal([4, 1]), name='weight')
        b = tf.Variable(tf.random_normal([1]), name='bias')
        model = tf.global_variables_initializer()
        # 가설 설정
        hypothesis = tf.matmul(X, W) + b
        saver = tf.train.Saver()
        parser = reqparse.RequestParser()
        parser.add_argument('avg_temp', required=True, type=float )
        args = parser.parse_args()
        avg_temp = float(args['avg_temp'])

        with tf.Session() as sess:
            sess.run(model)
            save_path = 'cabbage/data/saved.ckpt'
            saver.restore(sess, save_path)
            data = ((avg_temp,))
            arr = np.array(data, dtype=np.float32)
            x_data = arr[0:4]
            dict = sess.run(hypothesis, feed_dict={X: x_data})
            print(dict[0])
        result = int(dict[0])
        return result



