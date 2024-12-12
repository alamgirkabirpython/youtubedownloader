import streamlit as st
from yt_dlp import YoutubeDL
import os
hide_github_icon = """
<style>
#GithubIcon {
  display: none;
}
</style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

# Set up the Streamlit page
st.set_page_config(page_title="YouTube,Pinterest and Facebook Downloader", layout="wide")

# Custom CSS for an attractive UI
st.markdown(
    """
    <style>
    .main-header {
        background-color: #FF5733;
        padding: 20px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-family: 'Arial', sans-serif;
    }
    .navbar {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin: 20px 0;
    }
    .navbar a {
        text-decoration: none;
        color: #FF5733;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .navbar a:hover {
        color: #FF2A00;
    }
    .navbar img {
        width: 24px;
        height: 24px;
        vertical-align: middle;
        margin-right: 8px;
    }
    .input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 30px;
    }
    .input-container input {
        padding: 15px;
        width: 70%;
        font-size: 1.2rem;
        border-radius: 5px;
        border: 2px solid #FF5733;
        margin-bottom: 20px;
        background-color: #FFFAF0;
    }
    .input-container select {
        padding: 15px;
        width: 70%;
        font-size: 1.2rem;
        border-radius: 5px;
        border: 2px solid #FF5733;
        margin-bottom: 20px;
        background-color: #FFFAF0;
    }
    .download-btn {
        padding: 15px 30px;
        background-color: #FF5733;
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .download-btn:hover {
        background-color: #FF2A00;
    }
    .footer {
        background-color: #FF5733;
        color: white;
        text-align: center;
        padding: 15px;
        margin-top: 20px;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header and Navbar with logos and links to features
st.markdown(
    """
    <div class="main-header">YouTube, Pinterest,TikTok, Instagram and Facebook Video/Audio Downloader</div>
    <div class="navbar">
        <a href="https://www.youtube.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube Logo" />
            YouTube
        </a>
        <a href="https://audiototexttospeech-gbtkqn6jtsahgttneny7app.streamlit.app/" target="_blank">
            <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxIQEhUTExMVFRUXFxcYFRgWFxcXFxcXFxUWGBYVFRcYHiggGBolGxUXITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGisdHyEtNzctMi0rLSsrKzctNzAtLTAvKy0tLS0tLSsrKystLysrLSstLzUrKy0tLTAtLS0tLf/AABEIAOEA4QMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAACAAMEBQYBBwj/xABHEAABAgMEBQcICAUCBwAAAAABAAIDBBEFEiExBhNBUXEUIjJhgZGxFjNykpOhwdEHFSNSU2LS8DRUVWThJEJDdIKiwuLx/8QAGgEBAQADAQEAAAAAAAAAAAAAAAECAwQFBv/EACwRAQACAgECBAQGAwAAAAAAAAABAgMRBBIxBSFBYRMiUfAjMnGBobEUM5H/2gAMAwEAAhEDEQA/APcVDi5lLWHepDGAgEhByWy7UM1s7UMY3TQYLsDnVrigGXzUiJkeBTcVoAqME0x5JAJQNqeEGrG4KMYh3oFG6RT0tl2rsNgIBITcY3ThggKa2JuX6SODzq1xRxWgCowKA35HgoSca8kjFSNWNwQE3JRY/SP72LhiHen4bQRU4lByWyPFKayCGMbpwwSgm9nigCB0h+9ilOyKbitAFQKFMCId6AFOZkOCHVjcFHdEIJxQKP0inJXIooTQRU4lBG5uWCAprLtTMHpBHBN444pyI0AVAxQOFQUYiHepOrG4IIa6perG5JAPJx1psxS3AbEXKepc1N7GuaDrG38Sk/mZbd6V+5hmudPqp8UCa+9gURhAY7kNy5jmu66uFM8EAcoPUndQOtBybr9y7yjqQC6KW4DYiY2/ieGC5qr2Nc0r1zDPag68XMtu9C15dgVx0UO20p2oGvumox9yB8wQMd2Kb5QepcdME7vFMY7/AHIJmoB3oHRC3AZBV8/bjYOBILtgGfbuWcnLWiRScTwGARNtm1zX4kjvXXENxaarzaatWHC85Fhs9JwquSltwoh+zjsJ/K+h7ldG3pLYhdgcijMEDHFZKz9IHQiNbzm/e2jitTDmw8AjEHI13qKXKD1JwQQcUPJuv3LuvphTJALohbgETBfz2blzV3sa0VVbVuw5KgdznOxArTBZVrNp1DG14rG7TqFs9tzEcELYhdgdqh2VajJxlW4Uz2qbqruNa0UmJidStbRaNwPUDrTXKD1I+UdS5ybr9yih156kkXJ+v3LqANQU42KBgdicvjeFGiNJJoEBvbexCUPmZ7UUE0GOHFcj40pjwQJ7w4UGaBsIjHclBFDU4cU894IOIyQc14TWoKbcCBUgrsWPXggcEwAKZkd3eo8V141K5VcVR1Q520GQsDVzjk0Z/wCAo2kFrCWhigrEebsNu87+AWQtXSaFCbqoZOudjGiHOu4bkF3P6TPh56tvUak9tEEHSt0Vhuso7K9s4hYdrxEcADWuJKutc2Ewk4NaMUQ7aM/DgMdFjPoNpzc47hvK8v0l04mZirYNYMLq6buJ+Cf0inXzkSprTKGwCuHAZlKX0LmogqQxnU53O7gisQ9xOZJ31JPihaaGowO8YLT2xozHlsYsPmnC+3nN79h2KmfJhBo9EtOYssRDjkxIOWOLmdYO0L2jRW1gyI2HeDoUQXoTq4b6L5ufKkLffR5ajjCiS7jzoVIsHgM2juKD6O14WI0n0nfAjGGzClDlnVaKzJoRYbHjEPaHA8Qsj9I8iA6HFG3mu7qivvW/jRWckRaNxLm5c3jFM0nUw2GjtsNmIIdt2rLfSVJ3rkcZN5ruBOHvUX6PZs33Q94qFrtIpMRZaI050wr1LO0fAz+XpLCk/wCTxvP1j+WO+jy0dXGMMnBw9/7C9IdEDhQZleK2PMGHFY7rFV7HLbDsWfPprJ1fVr8MydWKaz6SMQSndeEReN4UXVncVwvRSNeElHuHcUkAqZCyCOihxTiUBTOfYildvZ8Ucvl2oZnYgKYyUUPAIJ3pyC7HHcmYsS8a7NnzQdiRC7PuQJJKoSSSRNERjbRtFoizUw/nNl2aqENl8gOeR11IHYvJYjy95e7MmpV/bFoEyZFcYkzEJ9d/yCzbIlXtbvKDWWKy62pzP7Ci6STlfsxj1feccgpcJ9AOoKqab0fH/YK/9TvkFRb6P2W2FzjQxD0nbvyt3BbewJARXBpwCyclEWgs6eMMggqDQ6QWBC1TsKtIo5rsQQRivB7YskQIz4WxpBYTjzHZd2K9mtG23RW0JwXnGloDo7DvhuB7HNoise+TU7RhphTcF2wktPWHCmKfdARyUKkWGfzt8VR7PoJFrKBv4b4jPVeaDuou6ZypfLu23ecOqii/R8fspj/mYnwV9a/mIvoO8FlSdWifdhkjdJj2ee6GzFybh9eC9TtJtWkdRXj9gn/UQvS+C9kl+if3sXX4hH4kfo4PC53hmPd4lGbde4bnH3Fex2PFvy0N29oXkVsD7eL6bvFeoaIn/TwfRHgtnO/10lr8OnWXJCyCnLhCg1XmPXT0lBqkgLWu3p9jARUhc5OOtAYpbhuQKK66aDBdg86tcV1rb+J9yCYfqhUe9A3NEVujt+SaQFxDSTnQntTsrZ8NzGl7Q9xAJLhXPwCqBSUj6tg/hM9UJfVsH8NncENI6SkfVsH8NncEvq2D+GzuCGnzppW0wBGguwMKZdh+R5vNP/cqGx4t+YbuAr717F9KegpigzMrDqblyPCbhfYMQ9o2vC8W0baWxnh1QWgjHA4HaEG9lOcaKqZGpFiem73GittHhec7qA8VmbZi6icisO118cHY4KjTyswrOFNrIS051qfDnERo3znWqCffrIxOxjQ3tca/+Kbiz9BXHhvOwKVJyhazndJxvO4nZ2IIRgI5CB9qz0q92KmugJiarDhvcOldus63PwCK9J+jlv8Aomv/ABIkV/rRHU91Fb6QRLstFP5CO9FYUhyaXgwfw4bWniBiVV6dTF2Wu/fcB3YrPDXqyVj3ac9unHafZkdE4F+ZYN1T3BeqPjcyowwx4hee/R9ArGe/7radpW2m33WuJrS6e9dPPneXX0cvhtenBv6y8ntN9YsQ/nd4les6NQ7spC3hgXkV0vfTa53iV7PZwpDazZSnuWznzqK1afDI3a9zginepOqbuQagdaDlB6l5r1z2qbuSTPKD1JIC5QNy4YN7GuaDUOTzYgAocwgEPuYZqHORb7mt3Yn4KVEbeNRkoEIc5x66dyJIo3RdwPgrCU6DPRHgFXxui7gfBWEp5tnojwCpB1JUtr2TMxYl6FOPgtoBdaxhFd9SFC8np3+pRfZw/korTpLMeT07/Uovs4fyS8np3+pRfZw/kg0683+mSz2Nl2R2w2hwiNDnhoDqEUxIzWh8np3+pRfZw/kqXTHRWbiycYOnYkajC4MLGAOLRUDAV2KowOhUSsZzTtZ4FOfSBoq6ZYI0IViwxkM3t3DrCymittaiZhPODb111dgcbp7l7Y6BtHYiPnGDaL4RLXA1GYIoe0FWcra98hrQ5zjkGgk9y9otDR6WjmsWAx53kUPeEMpY0CB5qExnWBj3lBj7CsKIKRY4o4YsZ938zutXboKuXQE06AqKZ0BLR+R5XPQ4eOrl/tom4vyY3r30XdIJ0S7N73UDGjMk5ABbPQSwTJy/2nn4p1kY/mIHN4AYKDRrAafTt+M2GDgwY8T/AIW4n5tsGG6I40DRX5BeVsD5qPvdEfjwJ+AXfwcfzTkntDzfEsnyRjjvb7/tuNBZO5L3znENewYBTNK5kQ5WIdpAaOJNFZysAQ2NYMmgDuWM+kGeq5kEHLnO4nJasf42ffvtuyzHH42vpGlFoxJ66aht3G8ez/K9ebBuY50WC+jiSo98Zww6LfE+C9AfEDhQZpzb9WWfY8Px9GGPfzc5R1LnJ+tAIJT+vbvXI7jfJzvSTmvbvXEB3xvCjRGkk4FNqZCyCBtjrrTXDPNV0tlXeSfepVpZHh81EkxzG8AiSON0XcD4KwlPNs9EeAVfG6LuB8FYSnm2eiPBUhWWrYr4z77ZqPCFALsNwDcNuIzUTyZi/wBQm/Wb+lTrTsZsZ94x48PACkOKWN40CieTTP5qb9u5QB5Mxf6hN+u39KXkzF/qE367f0o/Jpn81N+3cl5NM/mpv27kAeTMX+oTfrt/SuHRiJ/PzfrN/SnPJpn81N+3cl5NM/mpv27kHz59J+ib7LmjQudCi1cx53k1cCd63f0WaXsmoTZWM4CPDFGEnzjRlT8wotxbmgMtOQjCjR5h4zbeil112xwBXgmlmg07ZUW9RzoYNWRodewmmLSqPoJ8t1Jl8uvH9HvpfmoLQyYY2YaMA7oxKdZydxWgd9NMtT+Ei19JlPFEbp0v1Kg0ktyDJtN4gv2NB8fksl5e2jaTtXJS5aDhVoqRsxecG961+iH0diE8TE67XRsHNbmxh3n7zutA3oLo1FjRBPzjaOzgQiOiD/xHDYaHLYvRElmtLNIhAaYUM1iHM/cHzWePHbJbpq15ctcVZtbsp9OLZ1jtQw81p5/W7d2KZoHZVAY7hngyu7a5Z7R2x3TUSmNwYvd8OJXqEKGGNDWigAoB1Lv5N64scYafu87iUtnyznv+337BmIzYbS9xoGgk9i8pm4zpqOSMXRHUA4nBajTu16AS7DnjE91GqPoHZV5xjuGDcGdZOZ7E40fBxTlt3nsnLtPIzVw17R3+/ZrbKlRAuwm7GDtIrUq1hNIIqFEhGkZvA/BWcbolebM7ncvXrERGodLxvCiXDuPcuBTlFQrh3H3pKakg5dG5RIpxK7rnb/BPMhgipGKBl4rDd2qDJnmN4BTJ0kAgYYKvs11YY6sFUk/G6LuB8FYSnQZ6I8Aq+N0XcD4KwlPNs9EeCEKu1rEl48S/Ee8OoBQRSwU4AqF5LSf4kT27vmn7bsWQjRL8xcv0A50S6aDLCqhwtE7LeaNDHHc2JU9wKB4aKyf4kT27vms3brpGXmYMqzXPjRnhgrGeGtFCS4mvUr12i0jC+01VA01FXOqTsoKqotiBBmnB0drDd6JNG3eoO2LKtZlja0QvfJaT/Eie3d80vJaT/Eie3d81DgaM2VdFdXWgr9t/7JzyZsnfC9qPmsWSR5LSf4kT27vmkdFZIggveQcwYziDxBKj+TNk74XtR+pLyZsnfC9qP1IGGfRfY7hhLMPWHHxVbb/0c2ZLQb8OVZevDpVd4rZWBZ0rAa4S12hNXXX3saDrTGmX8MfSHxQMaPy7IcBgYxrBTJoA2qwc4AVOAGah2N5lnD4lO2hLa2G+HWl4EV3Kx380nevJldINLwKsl8TkX7vRWbsiyos3EoK0rz3nGnzKvrO0Ife+2eLg2Nzd8lspSVZCaGMaGtGwL0bZ8WCvTi85+rya8bNyL9WfyiPQ3Zlnsl4YhsGAzO0naSo1v2s2VhFx6RwYN538E7a9qQ5Zl959FozcepeaT05FnItTi5xo1oyA2ALTx8E5bddu3r7ujlcmuCvRT83pH0KSlok3HDa1c81cdw2lepSMo2DDbDaMGin+VW6M2IJWHjjEdS8fgO9XKnLz/EtqvaF4XG+FXqt+ae6LGP2rO1WUE4hV8Bt6Yocgz4q2ewAVGa43dAyFDvHejEV29P6lu5FRaneuqTqW7kkA8nG8oTFLcNyLlA3FCYV7HegVy+Kngqezxdc9m51RwKuQ+5gVSzL7kcGlA4UPHYiSlxui7gfBWEp5tnojwVfG6LuB8FYSfm2eiPBUhTWzI2fFijlAgmKQAA9wDiNgAqnbPsKUgHWwoLGYUqM6bsSitWTgueHmGwxBTnEVIplQqptacIowHLE/ALkz8uuHv5t+PDNytieMQ02DABUk02A4Bscw7pIoIjg0E9WSkxI4c4AihPX/AIUd8aT1rWTD4JINbr8adi6ePysWavyS5suC9LfMtxZti/23tB+pL6usX+29oP1I9dY39t7ktdY39t7lkyB9XWL/AG3tB+pL6usX+29oP1I9dY39t7ktdY39t7kFxo/LybGu5Jq6E87VuDsabaFMaZfw59IfFSLBfKFruS6u7XnaulK0GdFH0y/hz6Q+KgCxvMs4fEqaoVjeZZw+JU1VCVBbmlEKXq1tHxNwyB/MVflYOJoXGdFPOFwkm9tx6t66OPXFMzOSdRH8ublXzVrEYo3M/wAKGLGjTkXGr3uyGwcBsC3mjWjrZYXnUMU5nY3qCnWRY8KWbRgx2uOZVgtnI5XXHRTyq08bhfDnryTu39EkkmZyNcY53UuN3m7MP2kSJ13R2K1ES9hvUGxoX2QG3M/vtU4QruO5RkLUDeUHKDuCPlA3IOTnegXKDuCSXJzvSQDqXbvBPMiAChzTl4b1EiDEoDiNvGoxCrrYl/syciKEdnBWkA0CCbbeFM80FXAj6yFe/Ka8aK0gxLsJpP3R4LNtJgPcw4NeCW8dysZiYq1jBsa2vGi15cnRXa0r1To1NzN0F5/+ncs5FiVJceJUu0pi86gyHiquZfs718zys3Xb9HrYqdMbRpiYa2rnuDW7Sdgy2Kxsu1rNLrz3wyGigqzEniRkis2XJoAKufgOC3MpIshsDboNBiaDE7SvW8L43RT4lu9v6cPKy9VumPRnPr+yd8H1B8kvr+yd8H1B8lqNQz7re4LuoZ91vcF6jlZb6/snfB9QfJL6/snfB9QfJajUM+63uCWoZ91vcEFfYU9KxmuMtcoDzropjQZ9ij6Zfw59IfFXbGAZADgFSaZfwx9IfFAFjeZZw+JU1QrG8yzgfEqaqhJJJIEkkkgSrZ+sWI2E3Ha74KZNzAhtLig0dgnnRX5uOFd2xFWUuy5ngKUTr3gigzXJjEYb01BGIUUhCdu8E/rm7/FEXDeod07igla5u/xSUW6dy6gFTIWQXbg3BRojiCUHZnPsRSu3sRQBUY4oJx4YK5AVJ2ZIIOkENrmgHOtVSzMe43rOAWZltOtfHjXmnUNddY8Ymozw2hWDbQZHq6G9rgMMCDTqI2HivI8Rvevp5ejt4tayUR9BVR4EO87HLMrkd9TwVjZcmYjmwxmcXncN37615nC408jNEekd2/kZfh13/wAX+jUnnFdwZw3q/QwoYaA0YACgRL6ry9HlR7kkkkikkkkgSo9Mv4c+kPirxUemX8OfSHxQBY3mWcPiVNUKxvMs4fEqaqxJJJJAlxzqCpSc4DEqnjxjMv1cPo/7nfAIDhNM1Fw82095V/HbSgG5RpeVEEXW4UopkvjWuPFRkGWz7E9G6JQTGAwwxTUIkkIACnIS0bgod87ygnJKFeO896SAtc7enmwwRU5lDycb1wxbuFMkHIjrpoMlltMp10VolIZOsi4YYFrTma9nuWrDL+OSyOlEryWJyqG0ueRd2kNGVadqk+zKsxE+bzTSqyzINfCl6xhDbsHOvHpEjGq80su1JiXiX4MRzXk47bxOxzTgV67BfU3iakmtd561XWlo9Bjm+GhsWhuvaMa0oCRtWvr35Wh3f4W69eKdp+iekXKS5sRlHQwLzh0HPOwbiPgvSdHZiBCZedFZfdniMBuXnVgWG6DDbLQDVwq6I87XE4kq88lJz77PerhwY8MTFI1twXva8xNp3p6B9cy/4rPWCX11L/is9YLzp1kTEE8+hHUFPk5BkTDWNB3EFbdMdtt9cy/4rPWCX11L/is9YLMDRon/AIje5d8mT99vcUGm+upf8VnrBL65l/xWesFmfJk/fb3FLyZP329xQab66l/xWesFSaV2rCiQhDY4OJIJpiAMcyonkyfvt7ius0ZNcYgptoEFrYvmWcPiVNQQYQY0NGQFAlFjNbiSAiDTUxMNhiriAFVzNuAm7CF9yUrYsSMb8Zx33diBsviTZusBbD2nfwV3IywgijfAJ+XpDFGtAT+orjXNRXYbA4VOaGKbuWCRiXcF0C/1URXIZvYFE+GGiozXC25jnsXBFvYb0ACMd6f1Ld3ig5ON6HlB3IHdS3d4pJvlB3JIC5QOtAYRdjvQal25PseAKFALXXMD7k3MQhGFKd/WiitvGoxXYPNrXBBj7b0Maavhm6erI8QsjFhxIDqRGGuTSMQSvYIrg4UGJUV0kCQXNyKaie7Kt7ViYrOtqbRKxDDh33UvPxPwC0fKB1omxGjamNUdyMSiS9/HCh3qpnrAhnZQ51CvGPAFDmm4ovGoxQZXkEzCP2bqj8y79bR4fnIVeC1UIXc8FyOxrxSgJVTTNM0kZ/ua4dicGkMHr7lamy2E1LfBEbMgbghpTu0jg9fcmnaQ16ENxVuLFYMmeCmQJaGwAUAIQ0y75yaiZNup2XsB8XGI8nq2LTRIYPRCKELueCbNIUlZLIGNBgp+uGVClEeCKDNNCEdyii5OepGIwGGOCPWt3qO6GSckBuhl2IXWm5nt3LsNwaKHNDGF7LFB1zr+A44oWwy3E7EoQumpwTkR4IoM0HNeOtByc9SEQjuUjWt3oGeTneEk9rW71xAdVEijEoFMhZBAMvkgmdnahmc+xFK7exAMAYp+IcDwQzGSjw8xxQcopoK6oBQHFGJT0tl2o4PRCZmc+xAUzsTcDNHK7U5MdEoCecDwUOi6zMcQpqAWlRow5x/exA7NSoHRCAZbLtXJnIIZrMcEpXMoBgjnD97FJccEMfon97VFbmECopjDgESgvzPEoDjjnFOS2RRwOiP3tTU1mEBzOXamoIxCKWz7E9G6JQESoVEgpyCDRJTkkEBTIWQSSQMTOfYildvYkkgOYyUeHmOKSSCaoBXUkEuD0QmZnPsSSQdldqcmOiVxJBHh5jiPFTUkkEF2alQOiEkkDU1n2JSuZSSQOx+if3tUVuYXUkE1QX5niupIJMDoj97U1NZhdSQcls+z4p6N0SuJIIozU5JJAkkkkH//2Q==" alt="Text-to-Speech Logo" />
            Text-to-Speech
        </a>
        <a href="https://audiototexttospeech-gbtkqn6jtsahgttneny7app.streamlit.app/" target="_blank">
            <img src="data:image/png;base64,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" alt="Subtitle Logo" />
            Subtitles
        </a>
        <a href="https://audiototexttospeech-kjbebvkre7e57yrodgmwxb.streamlit.app/" target="_blank">
            <img src="data:image/jpeg;base64,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" alt="Audio-to-Text Logo" />
            Audio-to-Text
        </a>
        <a href="https://www.tiktok.com" target="_blank">
            <img src="https://freepnglogo.com/images/all_img/1691751088logo-tiktok-png.png" alt="TikTok Logo" />
            TikTok
        </a>
        <a href="https://www.instagram.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram Logo" />
            Instagram
        </a>
        <a href="https://www.facebook.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook Logo" />
            Facebook
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Hero Image Section
st.image("https://images.pexels.com/photos/1573438/pexels-photo-1573438.jpeg", use_container_width=True)

# Input Section
st.markdown(
    """
    <h3 style="text-align: center; color: #FF5733; font-size: 1.5rem;">Paste your video link below</h3>
    <p style="text-align: center; color: gray; font-size: 1rem;">By using our service, you accept our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.</p>
    """,
    unsafe_allow_html=True,
)

# Input fields and download button
with st.container():
    video_url = st.text_input("Enter the video URL", placeholder="Paste your video link here...", key="video_url")
    format_option = st.selectbox("Choose Format", ["MP4", "MP3"], key="format_option")
    
    if st.button("Download", key="download", help="Click to download your video", use_container_width=True):
        if not video_url:
            st.error("Please enter a valid URL.")
        else:
            try:
                st.info("Downloading... Please wait.")
                download_dir = "downloads"
                os.makedirs(download_dir, exist_ok=True)

                ydl_opts = {
                    "format": "bestaudio/best" if format_option == "MP3" else "best",
                    "outtmpl": f"{download_dir}/%(title)s.%(ext)s",
                    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}] if format_option == "MP3" else [],
                }

                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    file_path = ydl.prepare_filename(info_dict)
                    if format_option == "MP3":
                        file_path = file_path.replace(f".{info_dict['ext']}", ".mp3")

                st.success("Download successful!")
                st.download_button(
                    label="Click here to download your file",
                    data=open(file_path, "rb"),
                    file_name=os.path.basename(file_path),
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Features Section
st.markdown(
    """
    ## How to Download?
    ### Follow these simple steps:
    1. Paste your video URL into the input box above.
    2. Select your preferred format (MP4 or MP3).
    3. Click on the "Download" button to save the video or audio.
    """,
    unsafe_allow_html=True,
)

# Footer Section
st.markdown(
    """
    <div class="footer">
        &copy; 2024 Video/Audio Downloader | Powered by Alamgir&trade; Safe Web
    </div>
    """,
    unsafe_allow_html=True,
)
