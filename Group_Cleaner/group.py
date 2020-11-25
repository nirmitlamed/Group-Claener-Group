from pyrogram.errors.exceptions.bad_request_400 import UserIdInvalid

def clean_group(c, m):
	n = 0
	for member in m.chat.iter_members():
		id = member.user.id
		stat = m.chat.get_member(id).status
		if stat not in ["creator", "administrator"]:
			m.chat.kick_member(id)
			m.chat.unban_member(id)
			n += 1
	m.reply(f'הוסרו {n} משתמשים')
	
	
def group(c, m):
	for new_member in m.new_chat_members:
		try:
			id = new_member.id
			kick = m.chat.kick_member(id)
			m.chat.unban_member(id)
			if type(kick) != bool:
				kick.delete()
		except UserIdInvalid:
			pass


	m.delete()
def service_messages(c, m):
		m.delete()
		