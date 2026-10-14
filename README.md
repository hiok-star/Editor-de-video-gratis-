# Video Editor

Advanced video editor built with **PySide6** (Qt) + **PyAV** (FFmpeg bindings).

## Features

- **Multi-track timeline** with video/audio tracks
- **Frame-accurate editing** with TimeCode support
- **Keyframe animation** for all parameters (opacity, position, color grading, effects)
- **Color grading** pipeline: curves, color balance, hue/saturation, LUT3D
- **Effects system**: blur, sharpen, vignette, noise, glitch (extensible)
- **Blend modes**: normal, multiply, screen, overlay
- **Hardware acceleration** support (D3D11, CUDA, QSV, DXVA2) via PyAV
- **Export** to MP4, MOV, AVI with configurable codecs/quality

## Architecture

```
video_editor/
├── core/
│   └── models.py          # Timeline, Track, Clip, Keyframe, Effect
├── render/
│   └── engine.py          # PyAV filter graph builder + render engine
├── ui/
│   ├── timeline.py        # Timeline widget (QGraphicsView-based)
│   └── preview.py         # Preview canvas + property panel
├── plugins/               # Plugin system (future)
├── main.py                # Main application
└── pyproject.toml         # Dependencies
```

## Installation

```bash
cd video_editor
pip install -e .[dev]
```

## Usage

```bash
python -m video_editor.main
```

Or:

```bash
python video_editor/main.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `←` / `→` | Previous/Next frame |
| `Ctrl+I` | Import media |
| `Ctrl+E` | Export video |
| `Ctrl+Z` / `Ctrl+Y` | Undo/Redo |
| `Del` | Delete selected clip |
| `Ctrl++` / `Ctrl+-` | Zoom timeline |

## Color Grading Parameters

Each clip supports animated color grading:

- **Brightness** (-1 to 1)
- **Contrast** (0 to 3)
- **Saturation** (0 to 3)
- **Hue** (-180 to 180°)
- **Lift/Gamma/Gain** (shadows/midtones/highlights, -1 to 1)
- **Curves** (per-channel RGB curves as string expressions)
- **LUT3D** (.cube file path)

## Effects

Built-in effects (add via Properties panel → "Add Effect"):

- **Blur** - Gaussian blur (radius)
- **Sharpen** - Unsharp mask (amount)
- **Vignette** - Darken edges (strength)
- **Noise** - Film grain (strength)
- **Glitch** - Digital glitch (intensity)

## Hardware Acceleration

Configure in **Tools → Render Settings**:

| Backend | Platform | Status |
|---------|----------|--------|
| `d3d11va` | Windows (Direct3D 11) | Experimental |
| `cuda` | NVIDIA GPU | Requires CUDA FFmpeg build |
| `qsv` | Intel QuickSync | Linux/Windows |
| `dxva2` | Windows (legacy) | Stable |

## Extending

### Custom Effects

```python
from core.models import Effect

# In render/engine.py, add to build_effect_chain:
elif effect.name == "my_effect":
    param = effect.get_parameter("param", time)
    my_filter = graph.add("my_ffmpeg_filter", f"option={param}")
    current.link_to(my_filter)
    current = my_filter
```

### Custom Transitions

Add blend modes in `render/engine.py` composite section.

## Roadmap

- [ ] Keyframe curve editor (bezier handles)
- [ ] Audio waveform display
- [ ] Proxy/preview generation
- [ ] Plugin API (Python + native)
- [ ] Multi-camera editing
- [ ] Motion tracking
- [ ] Text/title templates
- [ ] XML/EDL/AAF import/export

## License

MIT