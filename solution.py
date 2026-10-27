# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_PERSON_PER_DAY = 2


def _is_int(x):
    # True/False는 정수로 보지 않음
    return type(x) is int


class RoomBooking:
    def __init__(self):
        # (room, day) -> [(start, end, name), ...]
        self._bookings = {}

    # ---------- 채점 대상 메서드 ----------
    def book(self, room, day, start, end, name):
        if self.explain_book(room, day, start, end, name) is not None:
            return False
        self._bookings.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if self.explain_cancel(room, day, start, name) is not None:
            return False
        slots = self._bookings[(room, day)]
        for i, (s, _, _) in enumerate(slots):
            if s == start:
                del slots[i]
                return True
        return False

    def get_schedule(self, room, day):
        if room not in ROOMS or day not in DAYS:
            return []
        return sorted(self._bookings.get((room, day), []), key=lambda b: b[0])

    # ---------- 실패 이유 (웹 화면 안내용) ----------
    # 예약 규칙은 모두 여기 한 곳에만 있음. book/cancel도 이 함수로 판단함.
    # 성공할 수 있으면 None, 실패하면 이유 문장을 돌려줌. 아무것도 저장하지 않음.
    def explain_book(self, room, day, start, end, name):
        if room not in ROOMS:
            return f"없는 강의실이에요: {room} (A101 · A102 · B201만 가능)"
        if day not in DAYS:
            return f"없는 요일이에요: {day} (월~금만 가능)"
        if not (_is_int(start) and _is_int(end)):
            return "시각은 10, 11처럼 정수(시)로만 넣을 수 있어요"
        if start < OPEN_HOUR:
            return f"{start}시는 운영 전이에요. 9시부터 예약할 수 있어요"
        if end > CLOSE_HOUR:
            return f"{end}시는 운영 시간(9~21시)을 넘겨요. 21시까지 끝나야 해요"
        if start >= end:
            return "시작 시각이 끝 시각보다 빨라야 해요"
        if end - start > MAX_HOURS:
            return f"{end - start}시간은 안 돼요. 한 번에 3시간을 초과해서 예약할 수 없어요"

        for s, e, n in self._bookings.get((room, day), []):
            if start < e and s < end:  # 겹침 (끝나는 시각에 바로 시작은 허용)
                return f"{s}~{e}시 {n}님 예약과 시간이 겹쳐요"

        mine = []
        for r in ROOMS:
            for s, e, n in self._bookings.get((r, day), []):
                if n == name:
                    mine.append(f"{r} {s}~{e}시")
        if len(mine) >= MAX_PER_PERSON_PER_DAY:
            return (f"{name}님은 {day}요일에 이미 {len(mine)}건을 예약했어요 "
                    f"({', '.join(mine)}). 한 사람은 하루 2건까지만 예약할 수 있어요")
        return None

    def explain_cancel(self, room, day, start, name):
        if room not in ROOMS:
            return f"없는 강의실이에요: {room}"
        if day not in DAYS:
            return f"없는 요일이에요: {day}"
        if not _is_int(start):
            return "시작 시각은 10, 11처럼 정수(시)로만 넣을 수 있어요"
        for s, e, n in self._bookings.get((room, day), []):
            if s == start:
                if n != name:
                    return f"남의 예약은 취소할 수 없습니다 ({s}~{e}시는 {n}님의 예약이에요)"
                return None
        return f"{room} {day}요일 {start}시에 시작하는 예약이 없어요"
