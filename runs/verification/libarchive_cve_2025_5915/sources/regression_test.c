commit a612bf62f86a6faa47bd57c52b94849f0a404d8c
Author: Tobias Stoeckmann <stoeckmann@users.noreply.github.com>
Date:   Sun May 11 19:00:11 2025 +0200

    rar: Fix heap-buffer-overflow (#2599)
    
    A filter block size must not be larger than the lzss window, which is
    defined
    by dictionary size, which in turn can be derived from unpacked file
    size.
    
    While at it, improve error messages and fix lzss window wrap around
    logic.
    
    Fixes https://github.com/libarchive/libarchive/issues/2565
    
    ---------
    
    Signed-off-by: Tobias Stoeckmann <tobias@stoeckmann.org>
    Co-authored-by: Tim Kientzle <kientzle@acm.org>

diff --git a/libarchive/test/test_read_format_rar_overflow.c b/libarchive/test/test_read_format_rar_overflow.c
new file mode 100644
index 00000000..b39ed6b2
--- /dev/null
+++ b/libarchive/test/test_read_format_rar_overflow.c
@@ -0,0 +1,48 @@
+/*-
+ * Copyright (c) 2003-2025 Tim Kientzle
+ * All rights reserved.
+ *
+ * Redistribution and use in source and binary forms, with or without
+ * modification, are permitted provided that the following conditions
+ * are met:
+ * 1. Redistributions of source code must retain the above copyright
+ *    notice, this list of conditions and the following disclaimer.
+ * 2. Redistributions in binary form must reproduce the above copyright
+ *    notice, this list of conditions and the following disclaimer in the
+ *    documentation and/or other materials provided with the distribution.
+ *
+ * THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) ``AS IS'' AND ANY EXPRESS OR
+ * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
+ * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
+ * IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY DIRECT, INDIRECT,
+ * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
+ * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
+ * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
+ * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
+ * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
+ * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
+ */
+#include "test.h"
+
+DEFINE_TEST(test_read_format_rar_overflow)
+{
+    struct archive *a;
+    struct archive_entry *ae;
+    const char reffile[] = "test_read_format_rar_overflow.rar";
+    const void *buff;
+    size_t size;
+    int64_t offset;
+
+    extract_reference_file(reffile);
+    assert((a = archive_read_new()) != NULL);
+    assertEqualIntA(a, ARCHIVE_OK, archive_read_support_filter_all(a));
+    assertEqualIntA(a, ARCHIVE_OK, archive_read_support_format_all(a));
+    assertEqualIntA(a, ARCHIVE_OK, archive_read_open_filename(a, reffile, 1024));
+    assertEqualIntA(a, ARCHIVE_OK, archive_read_next_header(a, &ae));
+    assertEqualInt(48, archive_entry_size(ae));
+    /* The next call should reproduce Issue #2565 */
+    assertEqualIntA(a, ARCHIVE_FATAL, archive_read_data_block(a, &buff, &size, &offset));
+
+    assertEqualIntA(a, ARCHIVE_OK, archive_read_close(a));
+    assertEqualInt(ARCHIVE_OK, archive_read_free(a));
+}
