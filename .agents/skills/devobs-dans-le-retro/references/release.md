# Episode metadata, review and Transistor draft

## Identify and number

- Keep a private episode note with the recording ID, assigned number, known NyxMix project ID, Auphonic production UUID, Transistor episode ID and local paths. Match these against the recording, title, number and media when resuming.
- Use the Transistor show `devobs` as the source of truth. Check the regular numbered episodes, drafts and scheduled entries across enough pages to find the highest reservation. Retros and interviews share the sequence. Confirm the current season there. Older unnumbered Dev’Obs Actu episodes do not affect it. Reuse the number on a matching existing draft and recheck the reservation before creating a new one.
- Use `Dans le rétro : [sujet de la semaine]` as the title. In French show notes, introduce the topic and speakers and summarize what was actually discussed. Include agenda items only if present, with explicit dates where useful, and close with a clickable invitation. Confirm it still points to the community. [Discord Dev’Obs](https://discord.gg/kKUty5pfCQ)
- If a number is taken after rendering, reconcile the tags, filenames and draft number before upload. Correcting title, track or year in the final MP3 can be done without another Auphonic run.

## Review the final assets

- Keep the original Auphonic VTT. In a copy, correct obvious French punctuation and technical names without changing meaning, cue timings or speaker labels. Use local audio and paginated transcript segments when available. List uncertain words with timestamps. Check the new copy with `verify_vtt.py`, passing the actual MP3 duration from `ffprobe` when available.

  ```sh
  duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp3)"
  python3 /path/to/devobs-dans-le-retro/scripts/verify_vtt.py \
    original.vtt reviewed.vtt --duration "$duration"
  ```

- Derive chapter titles and timestamps from the processed audio and transcript. Keep the first chapter at zero and ensure starts increase and fit the final duration. Use the Transistor chapter editor or embed the chapters locally. Add `{{chapters}}` to the show notes if the chapter list belongs there. [Transistor chapter options](https://support.transistor.fm/en/article/how-do-i-add-mp3-chapters-to-my-podcast-episode-1ts9azc/)
- For a local chapter or tag correction, make a new MP3 using FFmpeg stream copy. If embedding chapters, put them in a UTF-8 `chapters.ffmetadata` file, with a `;FFMETADATA1` header and a `[CHAPTER]` section per chapter. Set `TIMEBASE=1/1000`, `START`, `END` and `title`. Use the next start as the end, or the final duration for the last chapter. Escape special characters according to FFmpeg’s format. `-map_metadata 0` preserves the master’s other tags.

  ```sh
  ffmpeg -v error -n -i auphonic.mp3 -f ffmetadata -i chapters.ffmetadata \
    -map 0:a:0 -map '0:v?' -map_metadata 0 -map_chapters 1 -c copy \
    -metadata "title=Dans le rétro : Sujet" -metadata "track=N" final.mp3

  ffprobe -v error -show_chapters -show_entries format=duration -of json final.mp3
  ffmpeg -v error -xerror -i final.mp3 -map 0:a:0 -f null -
  ffmpeg -v error -i auphonic.mp3 -map 0:a:0 -c copy -f streamhash -hash sha256 -
  ffmpeg -v error -i final.mp3 -map 0:a:0 -c copy -f streamhash -hash sha256 -
  ```

  The two audio stream hashes must match. Compare the probed duration and chapter start times with the reference. Add the applicable `date` or other corrected tags to the same command when needed. [FFmpeg metadata format](https://ffmpeg.org/ffmpeg-formats.html#Metadata-1)

## Save and verify a draft

- Upload the real final MP3 to the matching episode. In the dashboard, upload from the local file picker and choose **Save as a draft**. If the connected API exposes signed upload authorization, PUT the exact MP3 bytes with the required media type and use its returned `audio_url` for the draft. Keep signed URLs private. If the create response is ambiguous, search all statuses by title, episode number and media before retrying.
- Set the title, readable description, episode number, season and applicable explicit setting. Use the embedded chapters or enter processed-time chapters in the dashboard. Save the episode before adding the timed transcript. Use the connector if it accepts WebVTT uploads or go to **Transcripts → Upload a Transcript → Create Transcript** in the dashboard. If access is unavailable, deliver the reviewed VTT with that exact remaining step. [Transistor draft fields](https://support.transistor.fm/en/article/how-to-add-a-new-episode-to-your-podcast-1g8dmnt/), [Transistor transcript upload](https://support.transistor.fm/en/article/how-to-add-transcripts-to-your-podcast-episodes-1tau786/)
- Verify the confirmed draft has no publish date and media processing is complete. Check the chapter preview against the MP3, including seek and playback when browser access permits. When an exported Transistor VTT is available, compare every cue against the reviewed VTT with `verify_vtt.py --match-text`. If only paginated results are available, compare the full set of returned cues. Distinguish catalog verification, preview checks and listening in the handoff.
- If requested, create a square 3000 × 3000 JPEG cover for the current topic. Attach it only when in scope. Leave the episode as a draft unless the user separately requests scheduling or publication.
