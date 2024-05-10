import argparse
from src.stream_analyzer import Stream_Analyzer
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=None, dest='device',
                        help='pyaudio (portaudio) device index')
    parser.add_argument('--n_frequency_bins', type=int, default=400, dest='frequency_bins',
                        help='The FFT features are grouped in bins')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
                        help='when true process sleeps between frames to reduce CPU usage (recommended for low update rates)')
    return parser.parse_args()

def start_Stream():
    
    print("Stream started.")
    args = parse_args()

    audio = Stream_Analyzer(
                    device = args.device,        # Pyaudio (portaudio) device index, defaults to first mic input
                    rate   = None,               # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 60,    # Window size used for the FFT transform
                    updates_per_second  = 500,   # How often to read the audio stream for new data
                    smoothing_length_ms = 50,    # Apply some temporal smoothing to reduce noisy features
                    n_frequency_bins = args.frequency_bins, # The FFT features are grouped in bins
                    verbose   = args.verbose,    # Print running statistics (latency, fps, ...)
                    )

    fps = 60  #How often to update the FFT features + display
    last_update = time.time()
    print("All ready, starting audio measurements now...")
    fft_samples = 0

    while True:
        if (time.time() - last_update) > (1./fps):
            last_update = time.time()
            raw_fftx, raw_fft, binned_fftx, binned_fft = audio.get_audio_features()
            fft_samples += 1
            if fft_samples % 20 == 0:
                print(f"Got fft_features #{fft_samples} of shape {raw_fft.shape}")
        elif args.sleep_between_frames:
            time.sleep(((1./fps)-(time.time()-last_update)) * 0.99)


start_Stream()