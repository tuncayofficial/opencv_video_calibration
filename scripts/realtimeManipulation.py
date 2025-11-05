import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime

from effects.tracker import Tracker
from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.vhs import VHS

from processors.render_processor import RenderProcessor

def realtimeManipulation(args):
    ASSETS_PATH = 'assets/'

    # Effects
    tracker = Tracker()
    cc_manipulator = ColorChaosManipulator()
    vhs = VHS()

    entries = os.listdir(ASSETS_PATH)
    files = [entry for entry in entries if os.path.isfile(os.path.join(ASSETS_PATH, entry))]
    print("Files to be processed in assets folder : " + str(files))

    # I/O
    VIDEO_NAME_IO= str(input("Choose the video to process : "))
    VIDEO_PATH = ASSETS_PATH + VIDEO_NAME_IO + ".mp4"

    capture = cv.VideoCapture(VIDEO_PATH)
    output_frames = []
    FRAME_ORDER = 0

    while True:
        isTrue, frame = capture.read()  
        elapsed_time = time.time() - cc_manipulator.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(cc_manipulator.frames) // elapsed_time if elapsed_time > 0 else 0

        if not isTrue: 
            break
        
        if hasattr(args, "effects") and "ColorChaosManipulator" in args.effects:
            complexity = cc_manipulator.calculate_complexity(frame)

            if cc_manipulator.threshold is not None :
                cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "THRESHOLD : " + str(round(cc_manipulator.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "VHS EFFECT", (50, 350), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                if complexity > cc_manipulator.threshold :
                    cv.putText(frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else :
                    cv.putText(frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cc_manipulator.add_frame(frame)
            processed_cc_manipulator_frame = cc_manipulator.process_current_frame(frame, complexity)
            print("Processed frame number " + str(FRAME_ORDER))
            cv.imshow("PROCESSED VIDEO", processed_cc_manipulator_frame)
            FRAME_ORDER += 1

        elif hasattr(args, "effects") and "Tracker" in args.effects:
            complexity = tracker.calculate_complexity(frame)

            if tracker.threshold is not None :
                cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "THRESHOLD : " + str(round(tracker.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "VHS EFFECT", (50, 350), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                if complexity > tracker.threshold :
                    cv.putText(frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else :
                    cv.putText(frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
            tracker.add_frame(frame)
            processed_tracker_frame = tracker.process_current_frame(frame)
            print("Processed frame number " + str(FRAME_ORDER))
            cv.imshow("PROCESSED VIDEO", processed_tracker_frame)
            FRAME_ORDER += 1

        elif hasattr(args, "effects") and "VHS" in args.effects:
            complexity = vhs.calculate_complexity(frame)

            if vhs.threshold is not None :
                cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "THRESHOLD : " + str(round(vhs.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv.putText(frame, "VHS EFFECT", (50, 350), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                if complexity > vhs.threshold :
                    cv.putText(frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else :
                    cv.putText(frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            vhs.add_frame(frame)
            processed_vhs_frame = vhs.process_current_frame(frame, complexity)
            print("Processed frame number " + str(FRAME_ORDER))
            cv.imshow("PROCESSED VIDEO", processed_vhs_frame)
            FRAME_ORDER += 1
        else :
            print("Undefined argument.")
            break

        key = cv.waitKey(10) & 0xFF
        if key == ord('d'):
            print("D key detected!")
            break

    cv.destroyAllWindows()