FROM apache/superset:4.0.1

USER root

# 1️⃣ Cài authlib
RUN pip install --no-cache-dir authlib

# 2️⃣ Disable sourcemap để không tạo *.map khi build frontend
ENV GENERATE_SOURCEMAP=false

# 3️⃣ Build lại frontend (chỉ khi bạn đang tự build từ source)
# Nếu bạn dùng image official (đã build sẵn), có thể bỏ qua bước này
# RUN cd /app/superset-frontend && npm ci && npm run build

USER superset
