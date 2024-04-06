# file_integrity
Scripts to provide file hashing and system scanning for file changes

  - file hasher - wrapper around hashlib for use for file hashing in sys_health
  - file walker - wrapper around os.walk for use for system file traversal in sys_health
  - sys_health - file integrity check with hashes of traversed files to historical logs
