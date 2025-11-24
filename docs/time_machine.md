# macOS Time Machine Backup Setup Summary

**Device:** MacBook Air (macOS Sequoia 15.3)  
**Drive:** WD My Passport 0829 Media (HDD)

---

## 1. Drive Preparation
1. Open **Disk Utility** → enable *View ▸ Show All Devices*.
2. Select the top-level drive (e.g. *WD My Passport 0829 Media*).
3. Click **Erase**:
   - **Format:** Mac OS Extended (Journaled)
   - **Scheme:** GUID Partition Map
4. Partition the drive into:
   - **TimeMachine** — 512 GB (Mac OS Extended)
   - **Storage** — remaining space (Mac OS Extended or ExFAT)

**Result:** The physical drive uses GUID Partition Map and now appears in Finder as two volumes: *TimeMachine* and *Storage*.

---

## 2. Add to Time Machine
1. Open **System Settings → General → Time Machine**.
2. Click **Add Backup Disk...** and select **TimeMachine**.
3. Leave encryption optional (OFF for simplicity).
4. Allow the first backup to run automatically.

---

## 3. Power and Sleep Settings (macOS Sequoia 15.3)
**Path:** System Settings → Battery → Options...

| Setting | Recommended | Purpose |
|----------|--------------|----------|
| Prevent automatic sleeping on power adapter when the display is off | On | Keeps Mac awake for backups when plugged in. |
| Put hard disks to sleep when possible | Only on Battery | Prevents the external HDD from sleeping during backups. |

---

## 4. Verify Initial Backup
- Check Time Machine preferences for *“Latest backup: [time/date]”.*
- Finder → TimeMachine drive → `Backups.backupdb/<Mac Name>/<timestamp>`

**Verified backup:** 2025-10-28 at 11:12 PM (17.98 GB)

---

## 5. Checking Logs via Terminal

Show successful backup completion messages from the last 24 hours:
```bash
log show --predicate 'subsystem == "com.apple.TimeMachine" AND eventMessage CONTAINS "completed"' --info --last 24h
```

**Sample output:**
```bash
2025-10-28 23:12:35 backupd: Successfully completed backing up 17.98 GB...
```

To monitor live:
```bash
log stream --predicate 'subsystem == "com.apple.TimeMachine"' --info
```

Then in System Settings → Time Machine → click *Back Up Now*. Watch messages appear in real time. Press **Ctrl + C** in Terminal to stop.

---

## 6. Checking Automatic Backups
- **Menu bar:** Click Time Machine icon → shows latest backup time.
- **System Settings:** Time Machine panel updates hourly.
- **Finder:** New timestamped folders appear in `Backups.backupdb`.

---

## 7. Safe Eject and Maintenance
- Always eject both *TimeMachine* and *Storage* before unplugging.
- Keep the drive connected during desk use for hourly backups.
- Optionally check logs monthly to confirm success entries.

---

**Status:** Configuration complete and verified. Automatic hourly backups active as of 2025-10-28 23:12 (17.98 GB successful backup).
