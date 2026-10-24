
def build_user_prompt(teams:dict[str,str]):
    """
        builds user prompt dynamically with teams playing \n
        Note: data on teams playing should be in the form:  \n 
        { \n
        'home':'team-name', \n
        'away':'team-name' \n
        }
    """
    user_prompt = f"""
        Tell me about the upcoming game between {teams['home']} and {teams['away']}.
        Give me info on what players are out of the game.
    """

    return user_prompt
