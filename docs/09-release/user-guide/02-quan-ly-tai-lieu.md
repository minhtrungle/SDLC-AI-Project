# 02 — Quản lý tài liệu

## Tải lên tài liệu

![Tải lên nhiều file, một file sai định dạng](images/tai-len.png)

1. Bấm **+ Tải lên PDF** và chọn một hoặc **nhiều** file, **hoặc** kéo thả file vào ô viền nét đứt.
2. Mỗi file hiện thanh tiến độ (%) rồi chuyển thành *"đã tải lên"*.
3. File không hợp lệ hiện thông báo lỗi màu đỏ ngay cạnh tên; **các file hợp lệ khác trong cùng lượt vẫn được nhận**.

Yêu cầu với file:
- Định dạng **PDF** thật (đổi đuôi `.docx` thành `.pdf` cũng bị từ chối).
- Tối đa **20 MB** mỗi file (con số thực tế hiển thị trong ô kéo thả).
- Tối đa **50 tài liệu** trong workspace của bạn.
- PDF phải có **lớp văn bản**. PDF scan chỉ có ảnh sẽ báo *"Không trích xuất được văn bản"* — hãy chạy OCR trước khi tải lên.

## Trạng thái tài liệu

Sau khi tải lên, hệ thống đọc và lập chỉ mục tài liệu. Trạng thái tự cập nhật, **không cần tải lại trang**.

| Biểu tượng | Trạng thái | Ý nghĩa | Bạn nên làm |
|---|---|---|---|
| ◌ | **Đang xử lý** | Hệ thống đang đọc tài liệu | Chờ; tài liệu này chưa được dùng để trả lời |
| ✓ | **Sẵn sàng** | Có thể hỏi về tài liệu này | Đặt câu hỏi |
| ✕ | **Lỗi** | PDF hỏng hoặc không đọc được (kèm lý do) | Xóa, kiểm tra file rồi tải lại |
| ! | **Không trích xuất được văn bản** | PDF chỉ chứa ảnh | Xóa, OCR file rồi tải lại |

Mỗi tài liệu trong danh sách hiển thị: **tên file**, **trạng thái**, **thời điểm tải lên** và **số trang**.

Chỉ tài liệu **✓ Sẵn sàng** mới được dùng làm nguồn trả lời. Nếu bạn hỏi khi vẫn còn tài liệu đang xử lý, câu trả lời sẽ kèm lưu ý *"Một số tài liệu đang xử lý chưa được dùng để trả lời; câu trả lời có thể chưa đầy đủ."*

## Xóa tài liệu

1. Bấm nút **🗑** ở dòng tài liệu.
2. Hộp thoại **"Xóa tài liệu?"** hiện: *"…" sẽ bị xóa vĩnh viễn và không còn được dùng để trả lời câu hỏi.*
3. Bấm **Xóa** để xác nhận, hoặc **Hủy** để giữ lại.

Sau khi xóa:
- Tài liệu biến mất khỏi danh sách và **không bao giờ** được dùng để trả lời nữa.
- Các câu trả lời **cũ** từng trích dẫn tài liệu đó vẫn còn, nhưng nguồn được đánh dấu *"(tài liệu đã bị xóa)"*.
- Thao tác **không hoàn tác được** từ giao diện.

## Mẹo
- Đặt tên file dễ nhận biết (`HopDong_Alpha.pdf` tốt hơn `scan001.pdf`) — tên file xuất hiện trong mọi trích dẫn.
- Xóa phiên bản cũ khi tải phiên bản mới của cùng tài liệu, để tránh câu trả lời trích cả hai.
