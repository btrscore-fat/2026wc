import streamlit as st
import pandas as pd
import random
from typing import Dict, List, Tuple, Any

# ==========================================
# 📄 页面配置
# ==========================================
st.set_page_config(
    page_title="2026 美加墨世界杯模拟器",
    page_icon="🏆",
    layout="wide"
)

# ==========================================
# 🎨 自定义样式
# ==========================================
st.markdown("""
<style>
    .match-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: center;
    }
    .group-title {
        background-color: #1f77b4;
        color: white;
        padding: 5px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }
    .champion {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 10px;
    }
    .stMetric {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 📊 分组数据（官方确认的48队分组）
# ==========================================
GROUP_DATA = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curaçao", "Côte d'Ivoire", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}

# ==========================================
# 📊 球队基础数据
# ==========================================
TEAMS_BASE_DATA = {
    "Argentina": {"win_rate": 0.80, "fifa_ranking": 1, "continent": "South America", "market_value": 950000000, "star_player": "Lionel Messi"},
    "France": {"win_rate": 0.60, "fifa_ranking": 2, "continent": "Europe", "market_value": 1500000000, "star_player": "Kylian Mbappé"},
    "England": {"win_rate": 0.80, "fifa_ranking": 3, "continent": "Europe", "market_value": 1400000000, "star_player": "Harry Kane"},
    "Spain": {"win_rate": 0.80, "fifa_ranking": 4, "continent": "Europe", "market_value": 1200000000, "star_player": "Pedri"},
    "Brazil": {"win_rate": 0.70, "fifa_ranking": 5, "continent": "South America", "market_value": 1200000000, "star_player": "Vinícius Jr."},
    "Portugal": {"win_rate": 0.70, "fifa_ranking": 6, "continent": "Europe", "market_value": 980000000, "star_player": "Bruno Fernandes"},
    "Netherlands": {"win_rate": 0.70, "fifa_ranking": 7, "continent": "Europe", "market_value": 650000000, "star_player": "Virgil van Dijk"},
    "Belgium": {"win_rate": 0.30, "fifa_ranking": 8, "continent": "Europe", "market_value": 850000000, "star_player": "Kevin De Bruyne"},
    "Germany": {"win_rate": 0.70, "fifa_ranking": 9, "continent": "Europe", "market_value": 980000000, "star_player": "Jamal Musiala"},
    "Croatia": {"win_rate": 0.50, "fifa_ranking": 10, "continent": "Europe", "market_value": 450000000, "star_player": "Luka Modrić"},
    "Uruguay": {"win_rate": 0.60, "fifa_ranking": 11, "continent": "South America", "market_value": 480000000, "star_player": "Federico Valverde"},
    "Morocco": {"win_rate": 0.70, "fifa_ranking": 12, "continent": "Africa", "market_value": 320000000, "star_player": "Achraf Hakimi"},
    "Switzerland": {"win_rate": 0.50, "fifa_ranking": 13, "continent": "Europe", "market_value": 280000000, "star_player": "Granit Xhaka"},
    "USA": {"win_rate": 0.50, "fifa_ranking": 14, "continent": "North America", "market_value": 280000000, "star_player": "Christian Pulisic"},
    "Colombia": {"win_rate": 0.60, "fifa_ranking": 15, "continent": "South America", "market_value": 350000000, "star_player": "Luis Díaz"},
    "Japan": {"win_rate": 0.70, "fifa_ranking": 16, "continent": "Asia", "market_value": 220000000, "star_player": "Takefusa Kubo"},
    "Mexico": {"win_rate": 0.50, "fifa_ranking": 17, "continent": "North America", "market_value": 250000000, "star_player": "Santiago Giménez"},
    "Senegal": {"win_rate": 0.60, "fifa_ranking": 18, "continent": "Africa", "market_value": 380000000, "star_player": "Sadio Mané"},
    "Ecuador": {"win_rate": 0.50, "fifa_ranking": 19, "continent": "South America", "market_value": 220000000, "star_player": "Moisés Caicedo"},
    "Canada": {"win_rate": 0.50, "fifa_ranking": 20, "continent": "North America", "market_value": 180000000, "star_player": "Alphonso Davies"},
    "South Korea": {"win_rate": 0.60, "fifa_ranking": 21, "continent": "Asia", "market_value": 200000000, "star_player": "Son Heung-min"},
    "Australia": {"win_rate": 0.40, "fifa_ranking": 22, "continent": "Asia", "market_value": 140000000, "star_player": "Harry Souttar"},
    "Saudi Arabia": {"win_rate": 0.40, "fifa_ranking": 23, "continent": "Asia", "market_value": 120000000, "star_player": "Salem Al-Dawsari"},
    "Iran": {"win_rate": 0.60, "fifa_ranking": 24, "continent": "Asia", "market_value": 150000000, "star_player": "Mehdi Taremi"},
    "Norway": {"win_rate": 0.50, "fifa_ranking": 25, "continent": "Europe", "market_value": 500000000, "star_player": "Erling Haaland"},
    "Egypt": {"win_rate": 0.60, "fifa_ranking": 26, "continent": "Africa", "market_value": 250000000, "star_player": "Mohamed Salah"},
    "Tunisia": {"win_rate": 0.40, "fifa_ranking": 27, "continent": "Africa", "market_value": 160000000, "star_player": "Ellyes Skhiri"},
    "Austria": {"win_rate": 0.50, "fifa_ranking": 28, "continent": "Europe", "market_value": 250000000, "star_player": "David Alaba"},
    "Turkey": {"win_rate": 0.50, "fifa_ranking": 29, "continent": "Europe", "market_value": 300000000, "star_player": "Hakan Çalhanoğlu"},
    "Scotland": {"win_rate": 0.40, "fifa_ranking": 30, "continent": "Europe", "market_value": 200000000, "star_player": "Scott McTominay"},
    "Sweden": {"win_rate": 0.40, "fifa_ranking": 31, "continent": "Europe", "market_value": 260000000, "star_player": "Alexander Isak"},
    "Algeria": {"win_rate": 0.50, "fifa_ranking": 32, "continent": "Africa", "market_value": 180000000, "star_player": "Riyad Mahrez"},
    "Czech Republic": {"win_rate": 0.40, "fifa_ranking": 33, "continent": "Europe", "market_value": 180000000, "star_player": "Patrik Schick"},
    "Paraguay": {"win_rate": 0.40, "fifa_ranking": 34, "continent": "South America", "market_value": 120000000, "star_player": "Miguel Almirón"},
    "Qatar": {"win_rate": 0.40, "fifa_ranking": 36, "continent": "Asia", "market_value": 180000000, "star_player": "Akram Afif"},
    "Uzbekistan": {"win_rate": 0.50, "fifa_ranking": 37, "continent": "Asia", "market_value": 80000000, "star_player": "Eldor Shomurodov"},
    "Jordan": {"win_rate": 0.40, "fifa_ranking": 38, "continent": "Asia", "market_value": 60000000, "star_player": "Musa Al-Taamari"},
    "New Zealand": {"win_rate": 0.40, "fifa_ranking": 39, "continent": "Oceania", "market_value": 80000000, "star_player": "Chris Wood"},
    "Ghana": {"win_rate": 0.40, "fifa_ranking": 40, "continent": "Africa", "market_value": 200000000, "star_player": "Mohammed Kudus"},
    "Iraq": {"win_rate": 0.40, "fifa_ranking": 41, "continent": "Asia", "market_value": 50000000, "star_player": "Ali Adnan"},
    "Cape Verde": {"win_rate": 0.40, "fifa_ranking": 42, "continent": "Africa", "market_value": 60000000, "star_player": "Ryan Mendes"},
    "South Africa": {"win_rate": 0.40, "fifa_ranking": 43, "continent": "Africa", "market_value": 80000000, "star_player": "Percy Tau"},
    "Curaçao": {"win_rate": 0.30, "fifa_ranking": 44, "continent": "North America", "market_value": 40000000, "star_player": "Cuco Martina"},
    "Haiti": {"win_rate": 0.30, "fifa_ranking": 45, "continent": "North America", "market_value": 30000000, "star_player": "Duckens Nazon"},
    "Bosnia and Herzegovina": {"win_rate": 0.30, "fifa_ranking": 46, "continent": "Europe", "market_value": 100000000, "star_player": "Edin Džeko"},
    "Côte d'Ivoire": {"win_rate": 0.40, "fifa_ranking": 47, "continent": "Africa", "market_value": 150000000, "star_player": "Sébastien Haller"},
    "DR Congo": {"win_rate": 0.40, "fifa_ranking": 48, "continent": "Africa", "market_value": 100000000, "star_player": "Chancel Mbemba"},
    "Panama": {"win_rate": 0.30, "fifa_ranking": 49, "continent": "North America", "market_value": 50000000, "star_player": "Aníbal Godoy"},
}

# ==========================================
# ⚙️ 核心模拟器类
# ==========================================
class WorldCupSimulator:
    def __init__(self):
        self.teams_data = TEAMS_BASE_DATA.copy()
        self.groups = GROUP_DATA.copy()
        
    def get_team_stat(self, team_name: str, stat_key: str, default: Any = 50) -> Any:
        team = self.teams_data.get(team_name, {})
        return team.get(stat_key, default)
    
    def calculate_match_probability(self, team_a: str, team_b: str) -> Tuple[float, float]:
        rank_a = self.get_team_stat(team_a, 'fifa_ranking', 50)
        rank_b = self.get_team_stat(team_b, 'fifa_ranking', 50)
        
        score_a = max(1, 101 - rank_a) if rank_a else 50
        score_b = max(1, 101 - rank_b) if rank_b else 50
        
        rate_a = self.get_team_stat(team_a, 'win_rate', 0.5)
        rate_b = self.get_team_stat(team_b, 'win_rate', 0.5)
        
        final_a = score_a * (0.5 + rate_a)
        final_b = score_b * (0.5 + rate_b)
        
        total = final_a + final_b
        if total == 0:
            return 0.5, 0.5
        
        return final_a / total, final_b / total
    
    def simulate_match(self, team_a: str, team_b: str, is_knockout: bool = False) -> Tuple[Any, int, int, bool]:
        prob_a, prob_b = self.calculate_match_probability(team_a, team_b)
        
        rand = random.random()
        penalties = False
        winner = None
        goals_a = 0
        goals_b = 0
        
        if rand < prob_a:
            goals_a = random.randint(1, 4)
            goals_b = random.randint(0, goals_a - 1)
            winner = team_a
        elif rand < prob_a + prob_b:
            goals_b = random.randint(1, 4)
            goals_a = random.randint(0, goals_b - 1)
            winner = team_b
        else:
            if is_knockout:
                extra_rand = random.random()
                if extra_rand < 0.5:
                    goals_a = 1
                    goals_b = 0
                    winner = team_a
                elif extra_rand < 0.8:
                    goals_a = 0
                    goals_b = 1
                    winner = team_b
                else:
                    penalties = True
                    winner = random.choice([team_a, team_b])
            else:
                goals_a = random.randint(0, 3)
                goals_b = goals_a
                winner = None
        
        return winner, goals_a, goals_b, penalties
    
    def simulate_group_stage(self) -> Tuple[Dict, List]:
        standings = {}
        all_matches = []
        
        for group_name, teams in self.groups.items():
            table = []
            for team in teams:
                table.append({
                    "Team": team,
                    "P": 0, "W": 0, "D": 0, "L": 0,
                    "GF": 0, "GA": 0, "GD": 0, "Pts": 0
                })
            
            team_stats = {stats["Team"]: stats for stats in table}
            
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    team_a = teams[i]
                    team_b = teams[j]
                    
                    winner, goals_a, goals_b, _ = self.simulate_match(team_a, team_b, is_knockout=False)
                    
                    team_stats[team_a]["GF"] += goals_a
                    team_stats[team_a]["GA"] += goals_b
                    team_stats[team_b]["GF"] += goals_b
                    team_stats[team_b]["GA"] += goals_a
                    
                    if winner == team_a:
                        team_stats[team_a]["W"] += 1
                        team_stats[team_a]["Pts"] += 3
                        team_stats[team_b]["L"] += 1
                    elif winner == team_b:
                        team_stats[team_b]["W"] += 1
                        team_stats[team_b]["Pts"] += 3
                        team_stats[team_a]["L"] += 1
                    else:
                        team_stats[team_a]["D"] += 1
                        team_stats[team_b]["D"] += 1
                        team_stats[team_a]["Pts"] += 1
                        team_stats[team_b]["Pts"] += 1
                    
                    team_stats[team_a]["P"] += 1
                    team_stats[team_b]["P"] += 1
                    
                    all_matches.append({
                        "group": group_name,
                        "team_a": team_a,
                        "team_b": team_b,
                        "goals_a": goals_a,
                        "goals_b": goals_b,
                        "winner": winner
                    })
            
            for stats in team_stats.values():
                stats["GD"] = stats["GF"] - stats["GA"]
            
            standings[group_name] = sorted(
                team_stats.values(),
                key=lambda x: (x["Pts"], x["GD"], x["GF"]),
                reverse=True
            )
        
        return standings, all_matches
    
    def simulate_knockout_stage(self, standings: Dict) -> Dict:
        group_winners = []
        group_runners_up = []
        third_placed = []
        
        for group, table in standings.items():
            if len(table) > 0:
                group_winners.append({"Team": table[0]["Team"], "group": group})
            if len(table) > 1:
                group_runners_up.append({"Team": table[1]["Team"], "group": group})
            if len(table) > 2:
                third = table[2].copy()
                third["group"] = group
                third_placed.append(third)
        
        third_placed.sort(key=lambda x: (x["Pts"], x["GD"], x["GF"]), reverse=True)
        best_third = third_placed[:8]
        
        round32_teams = []
        round32_teams.extend(group_winners)
        round32_teams.extend(group_runners_up)
        for team in best_third:
            round32_teams.append({"Team": team["Team"], "group": team["group"]})
        
        r32_matches = []
        used_teams = set()
        
        for winner in group_winners:
            for candidate in round32_teams:
                if candidate["Team"] not in used_teams and candidate["Team"] != winner["Team"] and candidate["group"] != winner["group"]:
                    r32_matches.append({
                        "team_a": winner["Team"],
                        "team_b": candidate["Team"]
                    })
                    used_teams.add(winner["Team"])
                    used_teams.add(candidate["Team"])
                    break
        
        remaining = [t for t in round32_teams if t["Team"] not in used_teams]
        for i in range(0, len(remaining), 2):
            if i + 1 < len(remaining):
                r32_matches.append({
                    "team_a": remaining[i]["Team"],
                    "team_b": remaining[i + 1]["Team"]
                })
        
        knockout_results = {
            "round_of_32": [],
            "round_of_16": [],
            "quarter_finals": [],
            "semi_finals": [],
            "third_place": None,
            "final": None,
            "champion": None
        }
        
        # R32
        r32_winners = []
        for match in r32_matches:
            winner, ga, gb, penalties = self.simulate_match(match["team_a"], match["team_b"], is_knockout=True)
            knockout_results["round_of_32"].append({
                "team_a": match["team_a"],
                "team_b": match["team_b"],
                "goals_a": ga,
                "goals_b": gb,
                "winner": winner,
                "penalties": penalties
            })
            r32_winners.append(winner)
        
        # R16
        r16_winners = []
        for i in range(0, len(r32_winners), 2):
            if i + 1 < len(r32_winners):
                winner, ga, gb, penalties = self.simulate_match(r32_winners[i], r32_winners[i + 1], is_knockout=True)
                knockout_results["round_of_16"].append({
                    "team_a": r32_winners[i],
                    "team_b": r32_winners[i + 1],
                    "goals_a": ga,
                    "goals_b": gb,
                    "winner": winner,
                    "penalties": penalties
                })
                r16_winners.append(winner)
        
        # QF
        qf_winners = []
        for i in range(0, len(r16_winners), 2):
            if i + 1 < len(r16_winners):
                winner, ga, gb, penalties = self.simulate_match(r16_winners[i], r16_winners[i + 1], is_knockout=True)
                knockout_results["quarter_finals"].append({
                    "team_a": r16_winners[i],
                    "team_b": r16_winners[i + 1],
                    "goals_a": ga,
                    "goals_b": gb,
                    "winner": winner,
                    "penalties": penalties
                })
                qf_winners.append(winner)
        
        # SF
        sf_winners = []
        for i in range(0, len(qf_winners), 2):
            if i + 1 < len(qf_winners):
                winner, ga, gb, penalties = self.simulate_match(qf_winners[i], qf_winners[i + 1], is_knockout=True)
                knockout_results["semi_finals"].append({
                    "team_a": qf_winners[i],
                    "team_b": qf_winners[i + 1],
                    "goals_a": ga,
                    "goals_b": gb,
                    "winner": winner,
                    "penalties": penalties
                })
                sf_winners.append(winner)
        
        # Third Place
        if len(sf_winners) >= 2:
            sf1_loser = knockout_results["semi_finals"][0]["team_b"] if knockout_results["semi_finals"][0]["winner"] == knockout_results["semi_finals"][0]["team_a"] else knockout_results["semi_finals"][0]["team_a"]
            sf2_loser = knockout_results["semi_finals"][1]["team_b"] if knockout_results["semi_finals"][1]["winner"] == knockout_results["semi_finals"][1]["team_a"] else knockout_results["semi_finals"][1]["team_a"]
            
            third_winner, ga, gb, penalties = self.simulate_match(sf1_loser, sf2_loser, is_knockout=True)
            knockout_results["third_place"] = {
                "team_a": sf1_loser,
                "team_b": sf2_loser,
                "goals_a": ga,
                "goals_b": gb,
                "winner": third_winner,
                "penalties": penalties
            }
        
        # Final
        if len(sf_winners) >= 2:
            champion, ga, gb, penalties = self.simulate_match(sf_winners[0], sf_winners[1], is_knockout=True)
            knockout_results["final"] = {
                "team_a": sf_winners[0],
                "team_b": sf_winners[1],
                "goals_a": ga,
                "goals_b": gb,
                "winner": champion,
                "penalties": penalties
            }
            knockout_results["champion"] = champion
        
        return knockout_results


# ==========================================
# 📊 可视化函数
# ==========================================

def display_group_standings(standings: Dict):
    st.subheader("📊 小组赛积分榜")
    
    groups_list = list(standings.items())
    cols = st.columns(3)
    
    for idx, (group_name, table) in enumerate(groups_list):
        with cols[idx % 3]:
            st.markdown(f'<div class="group-title">Group {group_name}</div>', unsafe_allow_html=True)
            df = pd.DataFrame(table)
            display_cols = ["Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]
            available_cols = [col for col in display_cols if col in df.columns]
            
            if available_cols:
                st.dataframe(df[available_cols], hide_index=True, use_container_width=True)


def display_group_stage_matches(all_matches: List):
    if not all_matches:
        return
    
    for match in all_matches[:48]:
        winner_text = f"🏆 胜者: {match['winner']}" if match['winner'] else "🤝 平局"
        st.markdown(f"""
        <div class="match-card" style="margin: 3px 0; padding: 5px;">
            <b>{match['group']}组</b> | {match['team_a']} {match['goals_a']} - {match['goals_b']} {match['team_b']}<br>
            <small>{winner_text}</small>
        </div>
        """, unsafe_allow_html=True)


def display_knockout_results(knockout_results: Dict):
    st.subheader("🏆 淘汰赛阶段")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**🎯 三十二强赛**")
        for match in knockout_results.get("round_of_32", [])[:8]:
            score = f"{match['goals_a']} - {match['goals_b']}"
            if match.get('penalties'):
                score += " (P)"
            st.markdown(f"""
            <div class="match-card" style="font-size: 12px; margin: 3px 0; padding: 5px;">
                <b>{match['team_a'][:12]}</b> vs <b>{match['team_b'][:12]}</b><br>
                📊 {score}<br>
                ✅ {match['winner'][:12]}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**🎯 十六强赛**")
        for match in knockout_results.get("round_of_16", []):
            score = f"{match['goals_a']} - {match['goals_b']}"
            if match.get('penalties'):
                score += " (P)"
            st.markdown(f"""
            <div class="match-card" style="font-size: 12px; margin: 3px 0; padding: 5px;">
                <b>{match['team_a'][:12]}</b> vs <b>{match['team_b'][:12]}</b><br>
                📊 {score}<br>
                ✅ {match['winner'][:12]}
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("**🎯 四分之一决赛**")
        for match in knockout_results.get("quarter_finals", []):
            score = f"{match['goals_a']} - {match['goals_b']}"
            if match.get('penalties'):
                score += " (P)"
            st.markdown(f"""
            <div class="match-card" style="font-size: 12px; margin: 3px 0; padding: 5px;">
                <b>{match['team_a'][:12]}</b> vs <b>{match['team_b'][:12]}</b><br>
                📊 {score}<br>
                ✅ {match['winner'][:12]}
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("**🎯 半决赛**")
        for match in knockout_results.get("semi_finals", []):
            score = f"{match['goals_a']} - {match['goals_b']}"
            if match.get('penalties'):
                score += " (P)"
            st.markdown(f"""
            <div class="match-card" style="font-size: 12px; margin: 3px 0; padding: 5px;">
                <b>{match['team_a'][:12]}</b> vs <b>{match['team_b'][:12]}</b><br>
                📊 {score}<br>
                ✅ {match['winner'][:12]}
            </div>
            """, unsafe_allow_html=True)
        
        if knockout_results.get("final"):
            st.markdown("**🏆 决赛**")
            final = knockout_results["final"]
            score = f"{final['goals_a']} - {final['goals_b']}"
            if final.get('penalties'):
                score += " (P)"
            st.markdown(f"""
            <div class="match-card" style="background-color: #ffd700; font-size: 14px;">
                <b>{final['team_a'][:15]}</b> vs <b>{final['team_b'][:15]}</b><br>
                📊 {score}<br>
                ✅ 冠军: {final['winner']}
            </div>
            """, unsafe_allow_html=True)


def display_champion(knockout_results: Dict):
    champion = knockout_results.get("champion")
    if champion:
        star_player = TEAMS_BASE_DATA.get(champion, {}).get("star_player", "Unknown")
        market_value = TEAMS_BASE_DATA.get(champion, {}).get("market_value", 0)
        
        st.markdown(f"""
        <div class="champion">
            <h1>🏆 世界冠军 🏆</h1>
            <h1 style="color: #c41e3a; font-size: 48px;">{champion}</h1>
            <p>⭐ 核心球星: {star_player}</p>
            <p>💰 球队身价: €{market_value/1000000:.0f}M</p>
            <p>🎉 恭喜 {champion} 夺得 2026 年美加墨世界杯冠军！ 🎉</p>
        </div>
        """, unsafe_allow_html=True)
        
        if knockout_results.get("final"):
            final = knockout_results["final"]
            st.markdown(f"""
            <div style="text-align: center; margin-top: 20px;">
                <h3>🏆 决赛战报 🏆</h3>
                <p style="font-size: 24px; font-weight: bold;">{final['team_a']} {final['goals_a']} - {final['goals_b']} {final['team_b']}</p>
                {"<p>⚽ 点球大战决胜 ⚽</p>" if final.get('penalties') else ""}
            </div>
            """, unsafe_allow_html=True)


def display_statistics(knockout_results: Dict):
    st.subheader("📈 赛事统计")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        champion = knockout_results.get("champion", "N/A")
        st.metric("🥇 冠军", champion if champion else "N/A")
    
    with col2:
        third_place = knockout_results.get("third_place")
        if third_place and isinstance(third_place, dict):
            st.metric("🥉 季军", third_place.get("winner", "N/A"))
        else:
            st.metric("🥉 季军", "N/A")
    
    with col3:
        total_goals = 0
        for phase in ["round_of_32", "round_of_16", "quarter_finals", "semi_finals", "final"]:
            matches = knockout_results.get(phase, [])
            for match in matches:
                if isinstance(match, dict):
                    total_goals += match.get("goals_a", 0) + match.get("goals_b", 0)
        st.metric("⚽ 淘汰赛总进球", total_goals)


# ==========================================
# 🚀 主程序入口
# ==========================================

def main():
    st.title("🏆 2026 美加墨世界杯模拟器")
    st.markdown("### 基于 FIFA 排名与球队数据的 48 强完整模拟")
    
    with st.sidebar:
        st.markdown("## ⚙️ 模拟设置")
        
        simulation_count = st.number_input("模拟次数", min_value=1, max_value=10, value=1)
        show_group_details = st.checkbox("显示小组赛详细比分", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 数据来源")
        st.info("📁 基于 FIFA 排名和历史胜率计算")
        
        st.markdown("---")
        st.markdown("### 🗺️ 主办国")
        st.markdown("🇺🇸 美国 | 🇨🇦 加拿大 | 🇲🇽 墨西哥")
        
        st.markdown("---")
        st.markdown("### 📋 分组信息")
        for group, teams in GROUP_DATA.items():
            st.markdown(f"**Group {group}**: {', '.join(teams[:2])}...")
    
    simulator = WorldCupSimulator()
    
    if st.button("🚀 开始模拟", use_container_width=True):
        with st.spinner("小组赛进行中... 🔥"):
            standings, group_matches = simulator.simulate_group_stage()
            
            display_group_standings(standings)
            
            if show_group_details:
                with st.expander("📋 查看所有小组赛详细比分"):
                    display_group_stage_matches(group_matches)
            
            st.divider()
            
            with st.spinner("淘汰赛进行中... ⚡"):
                knockout_results = simulator.simulate_knockout_stage(standings)
            
            display_knockout_results(knockout_results)
            
            st.divider()
            display_champion(knockout_results)
            
            display_statistics(knockout_results)
            
            if simulation_count > 1:
                st.info(f"已模拟 {simulation_count} 次，当前显示最后一次结果。")
    
    else:
        st.markdown("""
        ---
        ### 📖 使用说明
        
        1. **点击「开始模拟」按钮** 开始世界杯完整模拟
        2. 模拟包含 **小组赛（12组×4队）** + **淘汰赛（32强 → 决赛）**
        3. 比赛结果基于 **FIFA 排名** 和球队 **胜率数据** 计算
        4. 淘汰赛平局会进入 **加时赛** 和 **点球大战**
        
        ---
        ### 🏟️ 2026 世界杯新赛制
        
        - **48 支球队**，分为 12 个小组
        - 每组前 2 名 + **8 个最佳第三名** 晋级 32 强淘汰赛
        - 共进行 **104 场比赛**（小组赛 72 场 + 淘汰赛 32 场）
        """)
        
        top_teams = ["Argentina", "France", "England", "Spain", "Brazil", "Germany"]
        top_data = []
        for team in top_teams:
            if team in TEAMS_BASE_DATA:
                data = TEAMS_BASE_DATA[team]
                top_data.append({
                    "球队": team,
                    "FIFA排名": data["fifa_ranking"],
                    "胜率": f"{data['win_rate']*100:.0f}%",
                    "身价": f"€{data['market_value']/1000000:.0f}M",
                    "核心球员": data["star_player"]
                })
        
        if top_data:
            st.dataframe(pd.DataFrame(top_data), hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()