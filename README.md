# Motion Blur for LeviLauncher (Android)

Standalone extraction of the **Motion Blur** module from BedrockTools 1.5.10. The unrelated HUD, player, utility, and visual modules are not built.

## What is included

- Original Motion Blur implementation (`src/modules/visual/motionblur.cpp/.hpp`)
- The BedrockTools runtime, hook/signature/event and LeviLauncher Mod Menu support required by that implementation
- Android ARM64 xmake build
- `.levipack` packager and package verification
- Default Motion Blur settings

## Build with GitHub Actions

Push this repository to GitHub. The workflow at `.github/workflows/build.yml` runs on pushes to `main`/`master`, pull requests, tags beginning with `v`, and manual dispatch.

The job builds `libMotionBlur.so` for `arm64-v8a`, packages `dist/motionblur.levipack`, verifies the archive, and uploads both files as the `MotionBlur-Android-arm64` artifact.

## Local build

Requirements: Android NDK r28c, xmake, Python 3.12, and a working Android SDK/NDK installation.

```bash
xmake f -y -p android -a arm64-v8a -m release --ndk="$ANDROID_NDK_HOME"
xmake -y
LIBRARY="$(find build -type f -name 'libMotionBlur.so' -print -quit)"
python scripts/package_levipack.py --library "$LIBRARY" --output dist/motionblur.levipack
python scripts/verify_levipack.py dist/motionblur.levipack
```

## Install

Download `motionblur.levipack` from the GitHub Actions artifact (or a GitHub Release), then import it through LeviLauncher's native mod manager. The mod uses the `preload-native` package format and exposes its Motion Blur controls through the launcher's Mod Menu.

## Settings

- `intensity`: blur strength (0–5; default 0.9)
- `opacity`: blend amount (0–2; default 0.4)
- `samples`: sampling quality (4–8; default 6)
- `resolutionScale`: internal blur render scale (0.5–1; default 0.5)
- `depthBlur`: use depth information for movement blur (default true)

Settings are persisted in the mod's config directory by the inherited runtime config manager.

## Compatibility note

This source was extracted from BedrockTools 1.5.10 and retains its Minecraft function signatures and memory offsets. A successful CI build proves compilation and packaging only; it does **not** prove that those version-specific signatures match every Minecraft release or device. The manifest currently declares Minecraft `1.26.60.*`, matching the source archive metadata. Test on a backed-up game profile and update signatures/offsets if the target game build differs.

## Credits and license

Motion Blur is extracted from **BedrockTools 1.5.10** (original project by RadiantByte; source archive metadata credits MrPokeG). The implementation is rewritten native Android GLES code, with its camera-reprojection approach inspired by [Natural Motion Blur](https://github.com/ItsPasi/natural-motionblur-fabric/tree/1.20.6). This extraction keeps the original GPL-3.0 license and attribution. See `LICENSE` for the full license text.
