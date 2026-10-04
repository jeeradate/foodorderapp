[Welcome](../Welcome.md)
- หากใน ui.run() ไม่ได้ใส่พารามิเตอร์ reload=True ตัว Python Process จะทำงานด้วยโค้ดเดิมที่ถูก Load เข้าสู่ Memory ตั้งแต่ตอนเริ่มรัน เมื่อคุณกด Save ไฟล์ Python จึงไม่เกิดการ Reload ตัว Server ส่งผลให้ต้องหยุดและกด Run ใหม่เอง  เหมาะสำหรับการตั้งค่าระหว่างกำลังพัฒนา แต่ใน Production ควรเป็น reload=False เพราะข่วยประหยัด Resource และ Stable ได้แก้ไขถาวรแล้วใน core\config.py และ def main() ใน main.py [[ui.run reload]]

