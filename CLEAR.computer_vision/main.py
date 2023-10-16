# XXX A. XXX. Distribution is unlimited.

# XXX supported XXXnder XXX of XXX for 
# XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
# findings, XXX 
# of the author(s) XXX the XXX 
# XXX of XXX for XXX and XXX.

# © 2023 XXX.

# XXX.XXX-11 Patent Rights - XXX (May 2014)

# The software/XXX-Is basis

# XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
# XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
# XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
# XXX XXX.S. XXX may violate any copyrights that exist in this work.

from Worker import makeWorker
import socketio, sys, argparse, os

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default="obj")
    parser.add_argument('--testing', type=bool, default=False)

    defaultAddress = os.environ.get('WORKER_ADDRESS',
    "https://XXX.azurewebsites.net")

    parser.add_argument('--address', type=str,
    default=defaultAddress)
    
    args = parser.parse_args()
    workerType = args.type
    testing = args.testing
    workerAddress = args.address
    
    worker = makeWorker(workerType, workerAddress)

    if testing :
        worker.testing()
        exit()
     
    sio = socketio.Client()
    print(worker.apiURL)
    sio.connect(worker.apiURL)

    @sio.on("image_updated")
    def image_updated(message):
        if worker.ready :
            print('Server Update:', message)
            worker.runWorker()

    @sio.on("readiness_requested")
    def giveReady(message) :
        url = '{}/readyInfo'.format(workerAddress)
        worker.session.post(url, json={worker.identity: worker.identity})