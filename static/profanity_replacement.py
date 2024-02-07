profanity = {
	"fuck": "frick",
	"damn": "darn",
	"bitch": "dog",
	"shitty": "lousy",
	"whore": "tramp",
    "bastard": "scoundrel",
    "cock": "rod",
	"ass": "butt",
    
	"sex":"shenanigans"
}

def replaceProfanity(text):
	replaced_text = text
	for key, value in profanity.items():
		replaced_text = replaced_text.replace(key, value)
	return replaced_text
