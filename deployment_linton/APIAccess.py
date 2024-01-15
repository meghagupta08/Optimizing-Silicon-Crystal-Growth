import os
import cv2
import numpy as np
import urllib.request
from pathlib import Path
import os
import sys
from pprint import pprint

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
print("ROOT: \n",ROOT)
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


class Frame(object):
    def __init__(self):
        self.img = None
        self.headers = {}
        self.currentFrameNumber = None

    def add_header(self, key, val):
        self.headers.update({key: val})

    def set_image(self, image):
        self.img = image

    def get_image(self):
        return self.img

    def get_headers(self):
        return self.headers

    def get_frameNumber(self):
        return self.currentFrameNumber

    def set_framNumber(self, frameNumber):
        self.currentFrameNumber = frameNumber


# from oreilly.com/library/view/python-cookbook/0596001673/ch06s19.html
class RingBuffer:
    """ class that implements a not-yet-full buffer """

    def __init__(self, size_max):
        self.max = size_max
        self.data = bytearray()
        self.wcur = 0
        self.rcur = 0

    class __Full:
        """ class that implements a full buffer """

        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.wcur] = x
            self.wcur = (self.wcur + 1) % self.max

        def get(self):
            """ return list of elements in correct order """
            return self.data[self.rcur:] + self.data[:self.rcur]

        def get_n(self, n):
            if self.rcur + n < len(self.data):
                # no need to split
                retVal = self.data[self.rcur:self.rcur + n]
                self.rcur += n
            else:
                remBytes = n - (len(self.data) - self.rcur)
                retVal = self.data[self.rcur:] + self.data[:remBytes]
                self.rcur = remBytes
            return retVal

        def append_list(self, x):
            for v in x:
                self.append(v)

    def append(self, x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.wcur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full
            # print("FULL")

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data

    def get_n(self, n):

        #        if self.cur + n > len(self.data):
        retVal = self.data[self.rcur:self.rcur + n]
        self.rcur += n
        return retVal

    def append_list(self, x):
        for v in x:
            self.append(v)


class BufferedStream(object):
    """
    Buffer the reading from a stream so that blocks are read rather than bytes
    """

    def __init__(self, stream, blockSize, maxSize):
        self.blockSize = blockSize
        self.stream = stream
        self.buffer = RingBuffer(maxSize)
        self.index = 0
        self.bufferSize = 0

    def read(self, n):
        if n + self.index > self.bufferSize:
            nBlocks = n // self.blockSize + 1
            bytes = self.stream.read(self.blockSize * nBlocks)
            self.buffer.append_list(bytes)
            self.bufferSize += self.blockSize * nBlocks
        returnData = self.buffer.get_n(n)
        self.index += n
        return returnData


class EventLoop(object):
    """
        The event loop. This handles all of the reading of the image stream
        from the URL endpoint. Simple create a callback that accepts
        a Frame object argument. The callback is called whenever an image
        is read from the stream.
    """

    def __init__(self):
        self.callbacks = []
        self.stream = None
        self.maxFrameCount = 0

    def set_stream(self, stream):
        self.stream = stream

    def set_frame_count(self, count):
        self.maxFrameCount = count

    def add_callback(self, func):
        self.callbacks.append(func)

    def readLine(self, stream):
        data = ''
        byte = ''
        while byte != '\n':
            byte = stream.read(1).decode()
            data += byte

        return data

    def run(self):
        """
        The Main Loop entry point
        """
        if self.stream is None:
            raise Exception("Define the stream source before calling run() using set_stream()")

        stream = BufferedStream(self.stream, 1024, 200000)

        framesRead = 0
        line = ''
        currentFrame = None
        while True:
            if (self.maxFrameCount > 0) and (framesRead > self.maxFrameCount):
                break;
            try:
                line = self.readLine(stream).strip()
                while line != '--KrystalVision':
                    line = self.readLine(stream).strip()

                currentFrame = Frame()

                line = self.readLine(stream).strip()
                imageLength = 0
                while len(line) > 0:
                    sepIndex = line.find(':')
                    hdrName = line[0:sepIndex].strip()
                    value = line[sepIndex + 1:].strip()
                    currentFrame.add_header(hdrName, value)

                    if hdrName == 'Content-Length':
                        imageLength = int(value)

                    line = self.readLine(stream).strip()

                # Read the lines
                imageData = stream.read(imageLength)
                print(len(imageData), imageLength)
                # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE )
                img = cv2.imdecode(np.frombuffer(imageData, dtype=np.uint8), cv2.IMREAD_COLOR)
                currentFrame.set_image(img)

                framesRead += 1
                currentFrame.set_framNumber(framesRead)

                if img is not None:
                    yield currentFrame.get_image()
                    # for cb in self.callbacks:
                    #     cb(currentFrame)
                else:
                    pass
                    raise StopIteration
            except Exception as e:
                pass
                raise StopIteration


# define some callbacks...
def display_img(frame):
    cv2.imshow('Window name', frame.get_image())  # display image while receiving data
    if cv2.waitKey(300) == 27:  # if user hit esc
        exit(0)  # exit program

def get_single_image(frame):
    im = frame.get_image()
    #print(type(im))
    return im

def print_headers(frame):
    print(frame.get_headers())


def saveImage(frame):
    print(os.getcwd())
    curr_dir = os.getcwd()
    image_dir = curr_dir + "/images"

    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    fileName = image_dir + "/img_" + str(frame.get_frameNumber()) + ".png"
    cv2.imwrite(fileName, frame.get_image())


def setup_http_request(url, width, height):
    query = 'width={}&height={}'.format(width, height)
    endpoint = '{}/cropped_aipngstream'.format(url)
    requestUrl = endpoint + '?' + query
    print(requestUrl)

    return urllib.request.urlopen(requestUrl)


def main(arg_dict):
    # parser = argparse.ArgumentParser(description="A simple utility to access image stream in a frame-by-frame manner")
    # parser.add_argument('source', default='http://192.168.73.128:8888', help="The url of the source (file path or http://)")
    # parser.add_argument('-W', '--width', default=200, help="The width of the image to retrieve")
    # parser.add_argument('-H', '--height', default=200, help="The height of the image to retrieve")
    # parser.add_argument('-N', '--number', default=-1, type=int, help='The number of frames to read before exiting')
    #
    # args = parser.parse_args()

    source = arg_dict['source']
    print(source)
    stream = None
    if "http" in source:
        stream = setup_http_request(source, arg_dict['width'], arg_dict['height'])
        print('Reading from {} at ({}, {})'.format(source, arg_dict['width'], arg_dict['height']))
    else:
        print("source\n",source)
        pprint(sys.path)
        stream = open(os.path.join(ROOT,source),'rb')
        # stream = open(r'C:\Users\mxggis\Documents\PythonScripts\Deployment_application_linton\deployment_linton\aipngstream_endpoint.dat','rb')
        # stream = open(source, 'rb')

        # stream = open(ROOT/source)
        print('Reading from file: {}. Ignoring any width or height arguments'.format(source))

    if stream is None:
        # we shouldn't get here.
        print('Invalid source provided')
        exit()

    mainLoop = EventLoop()
    #mainLoop.add_callback(display_img)
    # mainLoop.add_callback(print_headers)
    # mainLoop.add_callback(saveImage)
    mainLoop.add_callback(get_single_image)
    mainLoop.set_stream(stream)
    mainLoop.set_frame_count(arg_dict['number'])
    # for eachFrame in mainLoop.run():
    #     print(type(eachFrame))
    #     time.sleep(5)
    return mainLoop.run()



def get_API_stream_images(arg_dict):
    return main(arg_dict)


# if __name__ == "__main__":
#     arg_dict = {}
#     arg_dict['source'] = 'cropped_stream.2.dat'
#     arg_dict['width'] = 250
#     arg_dict['height'] = 350
#     arg_dict['number'] = -1
#     main(arg_dict)