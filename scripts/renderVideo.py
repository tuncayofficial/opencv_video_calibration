import cv2 as cv
import argparse
import time
import subprocess
import os
import sys
from datetime import datetime

# ------------------- Importing effects from here -------------------
from effects.tracker import Tracker
from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.vhs import VHS

from effects.effect_manager import EffectManager

# ------------------- Importing functions from here -------------------
from processors.render_processor import RenderProcessor

def renderVideo(args):
    # ------------------- Initialize file from here -------------------
    ASSETS_PATH = 'assets/'
    FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"

    entries = os.listdir(ASSETS_PATH)
    files = [entry for entry in entries if os.path.isfile(os.path.join(ASSETS_PATH, entry))]
    print("Files to be processed in assets folder : " + str(files))

    VIDEO_NAME_IO = input(str("Enter video name to process : "))

    capture = cv.VideoCapture(ASSETS_PATH + VIDEO_NAME_IO + ".mp4")

    # ------------------- Initialize effects from here -------------------
    tracker = Tracker()
    cc_manipulator = ColorChaosManipulator()
    vhs = VHS()

    effectManager = EffectManager()

    # ------------------- Initialize processors from here -------------------
    renderProcessor = RenderProcessor()

    print("⚡ Processing frames at MAXIMUM SPEED (no display)...")

    frame_count = 0

    while True:
        isTrue, frame = capture.read()  

        fps_cv = capture.get(cv.CAP_PROP_FPS)
        max_frames = int (fps_cv * 30)

        if not isTrue or frame_count >= max_frames: 
            break
        
        frame_count += 1
        
        if frame_count % 30 == 0:
            elapsed = time.time() - active_effect.start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"📊 Processed {frame_count} frames ({fps:.1f} fps)")
        
        if hasattr(args, "effects"):
            if "Tracker" in args.effects:
                effectManager.set_effect("tracker")      
            elif "ColorChaos" in args.effects:
                effectManager.set_effect("color_chaos")
            elif "VHS" in args.effects:
                effectManager.set_effect("vhs")
            elif "FacialArtifacts" in args.effects:
                effectManager.set_effect("facial_artifacts")
            elif "NightVision" in args.effects:
                effectManager.set_effect("night_vision")
            elif "ChromaticAberration" in args.effects:
                effectManager.set_effect("chromatic_aberration")
            elif "Grunge" in args.effects:
                effectManager.set_effect("grunge")
            elif "None" in args.effects:
                effectManager.set_effect("none")
        else:
            print("Undefined argument.")
            break
         
        active_effect = effectManager.get_active_effect()
        elapsed_time = time.time() - active_effect.start_time

        complexity = active_effect.calculate_complexity(frame)
        active_effect.add_frame(frame)

        processed_frame = effectManager.process_frame(frame, complexity, args)
        active_effect.processed_frames.append(processed_frame)

        # <--------------------- Debugging text from here --------------------->
        
        if args.debug:
            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if active_effect.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_effect.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if complexity > active_effect.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv.putText(processed_frame, f"EFFECT: {effectManager.effect_history[-1].name}", (50, 350), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  

    capture.release()

    if active_effect.processed_frames:
        total_time = time.time() - active_effect.start_time
        print(f"✅ Processed {len(active_effect.processed_frames)} frames in {total_time:.2f}s")
        print(f"📹 Exporting at {len(active_effect.processed_frames)/total_time:.1f} fps...")
        renderProcessor.renderFrames(active_effect.processed_frames, "build/" + FILENAME, fps_cv)
        print("🎬 Video exported: " + FILENAME)
    else:
        print("❌ No frames processed!")

    print(f"🎉 Done! Open {FILENAME} to see your masterpiece!")
