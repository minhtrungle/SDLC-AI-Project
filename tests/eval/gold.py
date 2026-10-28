"""Synthetic gold set (PD-04). Must be re-run with the business team's real set (DEP-002) before go-live.

Each document is a list of page texts. Each question has:
  expect = (document name, page, substring that must appear in the answer)  or  None for "not found".
"""

DOCUMENTS = {
    "HopDong_Alpha.pdf": [
        "Hợp đồng Alpha được ký giữa Công ty An Phát và Công ty Bình Minh vào ngày 05/01/2026.",
        "Giá trị hợp đồng Alpha là 2,5 tỷ đồng, thanh toán làm 3 đợt.",
        "Thời hạn hợp đồng Alpha là 12 tháng kể từ ngày ký. Bên B chịu phạt 5% nếu giao hàng chậm.",
    ],
    "DuAn_Beta.pdf": [
        "Dự án Beta triển khai hệ thống kho vận tại Đà Nẵng cho khách hàng Hải Âu Logistics.",
        "Ngân sách dự án Beta là 900 triệu đồng. Dự án Beta kéo dài 6 tháng.",
        "Trưởng dự án Beta là ông Trần Minh Quân, số điện thoại liên hệ 0905 111 222.",
    ],
    "BangGia_2026.pdf": [
        "Bảng giá dịch vụ năm 2026: phí bảo trì hằng năm là 120 triệu đồng cho mỗi hệ thống.",
        "Phí đào tạo người dùng là 15 triệu đồng mỗi khóa, tối đa 20 học viên.",
    ],
    "QuyTrinh_NghiemThu.pdf": [
        "Quy trình nghiệm thu gồm ba bước: kiểm tra tài liệu, chạy thử, ký biên bản.",
        "Biên bản nghiệm thu phải có chữ ký của giám đốc kỹ thuật hai bên.",
    ],
    "ChinhSach_BaoHanh.pdf": [
        "Thời gian bảo hành phần cứng là 24 tháng kể từ ngày nghiệm thu.",
        "Yêu cầu bảo hành được phản hồi trong vòng 4 giờ làm việc.",
    ],
    "DeXuat_Gamma.pdf": [
        "Đề xuất Gamma xây dựng cổng thông tin khách hàng trên nền tảng web.",
        "Chi phí dự kiến của đề xuất Gamma là 1,2 tỷ đồng, dự kiến hoàn thành trong quý 3 năm 2026.",
    ],
}

QUESTIONS = [
    ("Giá trị hợp đồng Alpha là bao nhiêu?", ("HopDong_Alpha.pdf", 2, "2,5 tỷ")),
    ("Hợp đồng Alpha ký ngày nào?", ("HopDong_Alpha.pdf", 1, "05/01/2026")),
    ("Thời hạn hợp đồng Alpha bao lâu?", ("HopDong_Alpha.pdf", 3, "12 tháng")),
    ("Mức phạt giao hàng chậm của hợp đồng Alpha?", ("HopDong_Alpha.pdf", 3, "5%")),
    ("Dự án Beta triển khai ở đâu?", ("DuAn_Beta.pdf", 1, "Đà Nẵng")),
    ("Khách hàng của dự án Beta là ai?", ("DuAn_Beta.pdf", 1, "Hải Âu")),
    ("Ngân sách dự án Beta là bao nhiêu?", ("DuAn_Beta.pdf", 2, "900 triệu")),
    ("Dự án Beta kéo dài bao lâu?", ("DuAn_Beta.pdf", 2, "6 tháng")),
    ("Ai là trưởng dự án Beta?", ("DuAn_Beta.pdf", 3, "Trần Minh Quân")),
    ("Số điện thoại trưởng dự án Beta?", ("DuAn_Beta.pdf", 3, "0905")),
    ("Phí bảo trì hằng năm là bao nhiêu?", ("BangGia_2026.pdf", 1, "120 triệu")),
    ("Phí đào tạo người dùng bao nhiêu một khóa?", ("BangGia_2026.pdf", 2, "15 triệu")),
    ("Một khóa đào tạo tối đa bao nhiêu học viên?", ("BangGia_2026.pdf", 2, "20 học viên")),
    ("Quy trình nghiệm thu gồm những bước nào?", ("QuyTrinh_NghiemThu.pdf", 1, "ba bước")),
    ("Biên bản nghiệm thu cần chữ ký của ai?", ("QuyTrinh_NghiemThu.pdf", 2, "giám đốc kỹ thuật")),
    ("Thời gian bảo hành phần cứng là bao lâu?", ("ChinhSach_BaoHanh.pdf", 1, "24 tháng")),
    ("Yêu cầu bảo hành được phản hồi trong bao lâu?", ("ChinhSach_BaoHanh.pdf", 2, "4 giờ")),
    ("Đề xuất Gamma xây dựng gì?", ("DeXuat_Gamma.pdf", 1, "cổng thông tin")),
    ("Chi phí dự kiến của đề xuất Gamma?", ("DeXuat_Gamma.pdf", 2, "1,2 tỷ")),
    ("Đề xuất Gamma dự kiến hoàn thành khi nào?", ("DeXuat_Gamma.pdf", 2, "quý 3")),
    ("gia tri hop dong alpha", ("HopDong_Alpha.pdf", 2, "2,5 tỷ")),
    ("ngan sach du an beta", ("DuAn_Beta.pdf", 2, "900 triệu")),
    # Not answerable from the documents (AC-304.1: >= 9/10 must be not_found)
    ("Thủ đô của nước Pháp là gì?", None),
    ("Lương giám đốc công ty là bao nhiêu?", None),
    ("Giá cổ phiếu hôm nay thế nào?", None),
    ("Ai phát minh ra bóng đèn điện?", None),
    ("Công thức hóa học của nước là gì?", None),
    ("Thời tiết Hà Nội ngày mai ra sao?", None),
    ("Kết quả trận bóng đá tối qua?", None),
    ("Hướng dẫn nấu phở bò?", None),
    ("Tỷ giá đô la Mỹ hôm nay?", None),
    ("Dân số Việt Nam năm 2020 là bao nhiêu?", None),
]

# Thresholds from BRD §12.1 / NFR-001, NFR-002
MIN_ACCURACY = 0.85
MIN_CITATION_ACCURACY = 0.90
MIN_NOT_FOUND_CORRECT = 9 / 10
MAX_P90_LATENCY_MS_LOCAL = 2000

# Paraphrases with synonyms the documents do not use. Reported, not gated: lexical retrieval is known to miss
# these (SAD risk R-01). They quantify the gap an embedding retriever would close once OQ-006 allows it.
PARAPHRASES = [
    ("Tổng tiền của hợp đồng Alpha?", ("HopDong_Alpha.pdf", 2, "2,5 tỷ")),
    ("Hợp đồng Alpha có hiệu lực mấy năm?", ("HopDong_Alpha.pdf", 3, "12 tháng")),
    ("Kinh phí cho dự án Beta?", ("DuAn_Beta.pdf", 2, "900 triệu")),
    ("Người phụ trách dự án Beta tên gì?", ("DuAn_Beta.pdf", 3, "Trần Minh Quân")),
    ("Chi phí duy trì hệ thống mỗi năm?", ("BangGia_2026.pdf", 1, "120 triệu")),
    ("Bảo hành thiết bị kéo dài bao lâu?", ("ChinhSach_BaoHanh.pdf", 1, "24 tháng")),
    ("Ngân sách đề xuất Gamma?", ("DeXuat_Gamma.pdf", 2, "1,2 tỷ")),
    ("Khi nào Gamma xong?", ("DeXuat_Gamma.pdf", 2, "quý 3")),
]
