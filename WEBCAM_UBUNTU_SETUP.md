# Webcam Setup on Ubuntu (Find Device Name and Confirm Streaming)

Use this guide when you do not know the webcam device name on Ubuntu.

## 1) Install required tools

```bash
sudo apt update
sudo apt install -y ffmpeg v4l-utils
```

## 2) Discover webcam devices

List all video nodes:

```bash
ls /dev/video*
```

Show device names and mapped nodes:

```bash
v4l2-ctl --list-devices
```

Example output:

```text
Integrated Camera: Integrated C (usb-0000:00:14.0-8):
        /dev/video0
        /dev/video1
```

Usually, the main camera stream is `/dev/video0`.

## 3) Confirm the selected webcam works

Quick preview test:

```bash
ffplay -f v4l2 -framerate 30 -video_size 640x480 /dev/video0
```

If a window opens with live video, the device is correct.

## 4) Check supported formats (optional)

```bash
v4l2-ctl -d /dev/video0 --list-formats-ext
```

Pick a supported resolution and frame rate for stable streaming.

## 5) Start RTP video streaming to RoboMesh server

```bash
ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i /dev/video0 \
  -an -vcodec libvpx -cpu-used 5 -deadline realtime -g 10 \
  -error-resilient 1 -auto-alt-ref 1 \
  -f rtp "rtp://127.0.0.1:5004?pkt_size=1200"
```

## 6) Confirm RTP sender is running

```bash
ss -lunp | rg 5004
```

You should see UDP port `5004` in use while `ffmpeg` is running.

## Troubleshooting

- `No such file or directory /dev/videoX`: pick a valid node from `ls /dev/video*`.
- `Device or resource busy`: another app is using the camera. Close it and retry.
- Black screen: try another node (`/dev/video1`, `/dev/video2`) and lower resolution.
- Permission denied: run as a user in the `video` group or use elevated privileges.
