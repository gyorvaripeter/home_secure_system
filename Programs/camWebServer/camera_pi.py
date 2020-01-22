#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camera_pi.py
#  
#  
#  
import time
import io
import threading
import picamera


class Camera(object):
    thread = None  # Hatter folyamat, amely beolvassa a kepkockakat a kamerabol
    frame = None  # Az aktualis kepkockakat a hatter folyamat tarolja itt
    last_access = 0  # Az ugyfel utolso hozzaferesenek ideje a kamerahoz

    def initialize(self):
        if Camera.thread is None:
            # Elinditja a kepkockak hatter folyamatat
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # Var, amig a kepkockak rendelkezesre nem allnak
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # Kamera beallitasa
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # Hagyja, hogy a kamera bemelegedjen
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # Tarolja a kepkockakat
                stream.seek(0)
                cls.frame = stream.read()

                # Visszaallitja a steamet a kovetkezo kepkockanak
                stream.seek(0)
                stream.truncate()

                # Ha az elmult 10 masodpercben nem volt olyan ugyfel,
                # aki kepkockat kert, akkor allitsa le a folyamatot
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
