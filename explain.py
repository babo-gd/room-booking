# 웹 화면 안내용: 예약/취소가 "왜" 실패했는지 문장으로 알려줌.
#
# - 성공/실패 판단은 하지 않음. 판단은 항상 solution.py의 book / cancel 이 함.
#   웹은 book / cancel 이 False 를 돌려준 뒤에만 이 파일에 이유를 물어봄.
# - 강의실·요일·운영 시간·최대 시간 같은 값은 solution.py 에서 그대로 가져옴.
# - 예약 상태도 solution.py 의 RoomBooking 객체가 가진 것을 읽기만 함 (아무것도 바꾸지 않음).

from solution import ROOMS, DAYS, OPEN_HOUR, CLOSE_HOUR, MAX_HOURS, MAX_PER_PERSON_PER_DAY

FALLBACK = "예약 규칙에 맞지 않아요"


def _is_int(x):
    return type(x) is int


def _slots(rb, room, day):
    return rb.get_schedule(room, day)


def explain_book(rb, room, day, start, end, name):
    if room not in ROOMS:
        return f"없는 강의실이에요: {room} ({' · '.join(ROOMS)}만 가능)"
    if day not in DAYS:
        return f"없는 요일이에요: {day} ({DAYS[0]}~{DAYS[-1]}만 가능)"
    if not (_is_int(start) and _is_int(end)):
        return "시각은 10, 11처럼 정수(시)로만 넣을 수 있어요"
    if start < OPEN_HOUR:
        return f"{start}시는 운영 전이에요. {OPEN_HOUR}시부터 예약할 수 있어요"
    if end > CLOSE_HOUR:
        return f"{end}시는 운영 시간({OPEN_HOUR}~{CLOSE_HOUR}시)을 넘겨요. {CLOSE_HOUR}시까지 끝나야 해요"
    if start >= end:
        return "시작 시각이 끝 시각보다 빨라야 해요"
    if end - start > MAX_HOURS:
        return f"{end - start}시간은 안 돼요. 한 번에 {MAX_HOURS}시간을 초과해서 예약할 수 없어요"
    for s, e, n in _slots(rb, room, day):
        if start < e and s < end:
            return f"{s}~{e}시 {n}님 예약과 시간이 겹쳐요"
    mine = [f"{r} {s}~{e}시" for r in ROOMS for s, e, n in _slots(rb, r, day) if n == name]
    if len(mine) >= MAX_PER_PERSON_PER_DAY:
        return (f"{name}님은 {day}요일에 이미 {len(mine)}건을 예약했어요 ({', '.join(mine)}). "
                f"한 사람은 하루 {MAX_PER_PERSON_PER_DAY}건까지만 예약할 수 있어요")
    return FALLBACK


def explain_cancel(rb, room, day, start, name):
    if room not in ROOMS:
        return f"없는 강의실이에요: {room}"
    if day not in DAYS:
        return f"없는 요일이에요: {day}"
    if not _is_int(start):
        return "시작 시각은 10, 11처럼 정수(시)로만 넣을 수 있어요"
    for s, e, n in _slots(rb, room, day):
        if s == start:
            if n != name:
                return f"남의 예약은 취소할 수 없습니다 ({s}~{e}시는 {n}님의 예약이에요)"
            return FALLBACK
    return f"{room} {day}요일 {start}시에 시작하는 예약이 없어요"
