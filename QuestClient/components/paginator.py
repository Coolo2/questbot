import enum
import discord

class PaginatorView(discord.ui.View):

    def __init__(self, pages : list, embed : discord.Embed, index : int = 0, private = None):
        self.embed = embed
        self.pages = pages 
        self.index = index
        self.private : discord.User = private

        if self.embed.footer.text and "Page " not in self.embed.footer.text:
            self.embed.set_footer(text=f"{self.embed.footer.text} - Page {self.index+1}/{len(self.pages)}")
        else:
            self.embed.set_footer(text=f"Page {self.index+1}/{len(self.pages)}")

        super().__init__()

        self.children[1].disabled = self.index >= len(self.pages) - 1
        self.children[0].disabled = self.index <= 0

        
    
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="◀️", disabled=True)
    async def _left(self, interaction : discord.Interaction, button: discord.ui.Button):
        if self.private and interaction.user != self.private:
            return 

        embed = self.embed 

        self.index -= 1
        embed.description = self.pages[self.index]

        self.children[1].disabled = self.index >= len(self.pages) - 1
        self.children[0].disabled = self.index <= 0

        embed.set_footer(text=embed.footer.text.replace(f"Page {self.index+2}", f"Page {self.index+1}"))

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="▶️")
    async def _right(self, interaction : discord.Interaction, button: discord.ui.Button):
        if self.private and interaction.user != self.private:
            return 
        
        embed = self.embed 

        self.index += 1
        embed.description = self.pages[self.index]

        self.children[1].disabled = self.index >= len(self.pages) - 1
        self.children[0].disabled = self.index <= 0

        embed.set_footer(text=embed.footer.text.replace(f"Page {self.index}", f"Page {self.index+1}"))
            
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="🔎")
    async def _search(self, interaction : discord.Interaction, button : discord.ui.Button):
        if self.private and interaction.user != self.private:
            return 

        await interaction.response.send_modal(SearchModal(self))

class SearchModal(discord.ui.Modal):

    def __init__(self, paginator : PaginatorView):

        self.paginator = paginator

        super().__init__(title="Search", timeout=None)
    
    query = discord.ui.TextInput(placeholder='Enter search query here', label="Search Query", required=True, style=discord.TextStyle.short)

    async def on_submit(self, interaction : discord.Interaction):

        for i, page in enumerate(self.paginator.pages):
            
            if self.query.value.lower() in page.lower():
                embed = self.paginator.embed 

                prevIndex = self.paginator.index

                self.paginator.index = i
                embed.description = self.paginator.pages[self.paginator.index]

                self.paginator.children[1].disabled = self.paginator.index >= len(self.paginator.pages) - 1
                self.paginator.children[0].disabled = self.paginator.index <= 0

                embed.set_footer(text=embed.footer.text.replace(f"Page {prevIndex+1}", f"Page {self.paginator.index+1}"))
                    
                return await interaction.response.edit_message(embed=embed, view=self.paginator)
        
        return await interaction.response.send_message("Search query not found.", ephemeral=True)