# Auphonic postproduction

## Configure the production

- Look up the existing **Dev’Obs — Dans ton rétro** preset in the connected Auphonic account. The preset and its default basename still use the older wording. Set the episode title and deliverable basename to `Dans le rétro : [sujet]` and `devobs-N-dans-le-retro`. Set Track to the shared episode number and Year to the applicable year. If the subject is still uncertain, use provisional internal metadata and fix the exported tags later by stream copy.
- Save the production as a draft from the preset and attach each synchronized FLAC to the matching existing track. With MCP, use `create_production` without `track_names`, then use `upload_production_file` with the track ID from `check_status`. A bulk create call with `track_names` can replace the preset tracks. Use `edit_production` for `metadata.track`, year, title and summary when exposed. If the speaker roster changes, verify the treatment for every speech track before starting. In the dashboard, use the preset’s tracks and attach the local files directly.
- Read back the draft. The reference preset uses −16 LUFS, standard leveling, speech tracks with Studio Voice and Dynamic Denoiser, breath and reverb attenuation, applied silence and filler cuts, and French Whisper. Confirm the attached tracks, output basename, MP3 and VTT outputs, and empty production and output destinations. Confirm the intended processing if the account preset has changed. Leave the shared preset itself untouched.
- Record the production UUID in the private episode notes. If the connector supports a creation `request_id`, reuse the same ID and arguments after an uncertain response and look up the production before starting. Start a verified production once when authorized, using `start_production` for the existing draft with default restart and publication settings. Check its status until completion and resume via its UUID after an interruption. A slow or ambiguous response is a reason to check status before taking any action that might trigger another charge. [Auphonic multitrack production](https://auphonic.com/help/web/multitrack.html)

## Download and verify

- Download the original processed MP3 and WebVTT. Inspect `list_outputs` for exact filenames if using MCP. A private link returned by `download_output` may need the signed-in dashboard or the connector’s supported authenticated downloader. Save the actual files locally, and avoid putting private URLs or credentials in the episode notes.
- Verify that the MP3 decodes completely and the VTT has cues before making editorial copies. Measure loudness and true peak, and listen to the processed opening and ending if playback is available. Report decoder, loudness and listening checks separately.

  ```sh
  ffmpeg -hide_banner -nostats -xerror -i auphonic.mp3 -map 0:a:0 \
    -af ebur128=peak=true:framelog=verbose -f null -
  ```

- Use the processed master as the time reference from here on. When using Auphonic chapter data, use `start_output` or `start_output_sec` because applied cuts shift the timeline. [Auphonic output chapter timestamps](https://auphonic.com/help/api/query.html)
