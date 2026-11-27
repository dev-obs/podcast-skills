# Source recovery and editing

## Recover and identify

- Use the recording owner’s Craig link or `/recordings` and choose synchronized multitrack FLAC. If an Audacity project is supplied, keep its `.aup` file beside its `_data` folder or open the complete `.aup3` and export aligned stems. A download 403 can be an access problem. Try the signed-in Craig page, then request the archive or synchronized stems if needed.
- Map each file to the actual speaker and preserve the original starts, including offset silence. Different tail lengths can occur in a Craig export. Confirm that the selected edit interval fits all tracks before using a local trim. If track starts or offsets are unknown, reconstruct the timeline in the editor from trusted session data before trimming.

## Find the usable opening and ending

- On the shared timeline, use the user’s confirmed boundaries when they fit the sources. Otherwise use a Craig marker such as « début » to find the vicinity of the opening, then use speech context around it to locate the real greeting and identify the last intended sign-off. For an uncertain edge, keep the wider candidate and ask for the offset if the ambiguity affects the edit.
- Preview a short section across each cut from the source. The host’s first syllable or short lead-in can disappear even when a transcript looks complete. Listen for a natural onset, the full greeting, the other speaker’s reply, and intact last words. Local French ASR can locate candidate speech. Compare the source, trimmed stems and Auphonic master when diagnosing an abrupt opening, since automatic filler removal can change it after export. Report when the evidence is ASR or measurements only.
- Leave the body intact for this top-and-tail format. Apply the same start and end to all tracks in NyxMix or the equivalent editor. For ripple edits, cut the tail first or recalculate its position after the first cut. Export one untreated FLAC per speaker over the identical range, with no effects, normalization, sends or master processing. Use NyxMix’s stems render option when available.

## FFmpeg fallback for aligned FLACs

Use this when the stems already share a sample rate and sample 0 represents the same point in the recording. Determine the common start sample and exclusive end sample from the reviewed cut and sample rate. Keep the input and output paths distinct, and repeat the command with the **same** sample values for each stem.

```sh
# Example boundaries at 48 kHz. Replace both values for the current recording.
start_sample=720000
end_sample=5760000

ffmpeg -v error -n -i speaker-a.flac -map 0:a:0 -map_metadata -1 \
  -af "atrim=start_sample=${start_sample}:end_sample=${end_sample},asetpts=PTS-STARTPTS" \
  -c:a flac speaker-a-trimmed.flac

ffprobe -v error -select_streams a:0 \
  -show_entries stream=sample_rate,channels,start_time,time_base,duration_ts \
  -of json speaker-a-trimmed.flac
```

Check every export against the expected sample rate and length. With a FLAC stream time base of `1/sample_rate`, `duration_ts` should be `end_sample - start_sample`. Verify the speaker mapping and preview the trimmed edges again. Preserve the source channel layout unless there is a verified reason to extract a channel or downmix. [FFmpeg `atrim`](https://ffmpeg.org/ffmpeg-filters.html#atrim)
