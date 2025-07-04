import os
import re
import json
import uuid
import time
import random
import threading
import queue
import requests
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.logger import Logger

class TikTokReportBot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        
        # Variables
        self.proxies = []
        self.report_queue = queue.Queue()
        self.threads = []
        self.running = False
        self.paused = False
        self.report_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.total_reports = 0
        self.proxy_type = "http"
        self.session_cookies = None
        self.device_id = str(uuid.uuid4())
        self.session = requests.Session()
        
        # TikTok report reasons
        self.report_reasons = {
            "Illegal activities": 10000,
            "Harmful dangerous acts": 10001,
            "Hate speech": 10002,
            "Harassment and bullying": 10003,
            "Violent extremism": 10004,
            "Suicide self-harm": 10005,
            "Child safety": 10006,
            "Pornography": 10007,
            "Nudity": 10008,
            "Sexual solicitation": 10009,
            "Fraud scams": 10010,
            "Misinformation": 10011,
            "Privacy violation": 10012,
            "Intellectual property": 10013,
            "Spam": 10014,
            "Other": 10015
        }
        
        # Create UI
        self.build_ui()
        
        # Start GUI update handler
        Clock.schedule_interval(self.process_gui_updates, 0.1)
        
        self.log("Application started - Load proxies and authenticate first")

    def build_ui(self):
        # Header
        header = Label(
            text="TIKTOK MASS REPORT BOT", 
            font_size=24, 
            bold=True,
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            background_color=(1, 0, 0.3, 1)
        self.add_widget(header)
        
        # Main content
        main_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.9)
        
        # Left panel - Controls
        control_panel = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=10)
        
        # Authentication Section
        auth_frame = BoxLayout(orientation='vertical', size_hint_y=0.25)
        auth_frame.add_widget(Label(text="AUTHENTICATION", bold=True))
        
        # Session ID
        auth_frame.add_widget(Label(text="Session ID:"))
        self.session_id_input = TextInput(multiline=False, size_hint_y=0.2)
        auth_frame.add_widget(self.session_id_input)
        
        # Cookie Import
        auth_frame.add_widget(Label(text="OR Cookie File:"))
        self.cookie_chooser = FileChooserListView(size_hint_y=0.4)
        auth_frame.add_widget(self.cookie_chooser)
        
        # Auth Button
        auth_btn = Button(
            text="SET AUTHENTICATION", 
            size_hint_y=0.2,
            background_color=(0, 0.5, 0, 1)
        auth_btn.bind(on_press=self.set_authentication)
        auth_frame.add_widget(auth_btn)
        
        # Auth Status
        self.auth_status = Label(text="Not authenticated", color=(1, 0, 0, 1))
        auth_frame.add_widget(self.auth_status)
        
        control_panel.add_widget(auth_frame)
        
        # Proxy Settings
        proxy_frame = BoxLayout(orientation='vertical', size_hint_y=0.15)
        proxy_frame.add_widget(Label(text="PROXY SETTINGS", bold=True))
        
        proxy_type_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        proxy_type_layout.add_widget(Label(text="Type:"))
        self.proxy_type_spinner = Spinner(
            text='http', 
            values=('http', 'https', 'socks4', 'socks5'),
            size_hint_x=0.6
        )
        proxy_type_layout.add_widget(self.proxy_type_spinner)
        
        proxy_btn = Button(
            text="LOAD PROXIES", 
            size_hint_x=0.4,
            background_color=(0, 0.5, 0, 1)
        proxy_btn.bind(on_press=self.load_proxies)
        proxy_type_layout.add_widget(proxy_btn)
        proxy_frame.add_widget(proxy_type_layout)
        
        self.proxy_status = Label(text="0 proxies loaded", size_hint_y=0.2)
        proxy_frame.add_widget(self.proxy_status)
        
        control_panel.add_widget(proxy_frame)
        
        # Target Settings
        target_frame = BoxLayout(orientation='vertical', size_hint_y=0.25)
        target_frame.add_widget(Label(text="TARGET SETTINGS", bold=True))
        
        target_frame.add_widget(Label(text="Target URL:"))
        self.target_input = TextInput(
            text='https://www.tiktok.com/@tiktok/video/1234567890',
            multiline=False,
            size_hint_y=0.2
        )
        target_frame.add_widget(self.target_input)
        
        # Report Type
        report_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        report_layout.add_widget(Label(text="Report Type:"))
        self.report_type_spinner = Spinner(
            text='Video Report', 
            values=('Account Report', 'Video Report', 'Comment Report')
        )
        report_layout.add_widget(self.report_type_spinner)
        
        # Reason
        report_layout.add_widget(Label(text="Reason:"))
        self.reason_spinner = Spinner(
            text='Illegal activities', 
            values=list(self.report_reasons.keys())
        )
        report_layout.add_widget(self.reason_spinner)
        target_frame.add_widget(report_layout)
        
        # Threads/Reports
        count_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        count_layout.add_widget(Label(text="Threads:"))
        self.threads_input = TextInput(text='3', multiline=False)
        count_layout.add_widget(self.threads_input)
        
        count_layout.add_widget(Label(text="Reports:"))
        self.reports_input = TextInput(text='10', multiline=False)
        count_layout.add_widget(self.reports_input)
        target_frame.add_widget(count_layout)
        
        control_panel.add_widget(target_frame)
        
        # Control Buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.start_btn = Button(
            text="START REPORTING", 
            background_color=(0, 0.7, 0, 1)
        self.start_btn.bind(on_press=self.start_bot)
        btn_layout.add_widget(self.start_btn)
        
        self.pause_btn = Button(
            text="PAUSE", 
            background_color=(1, 0.8, 0, 1),
            disabled=True
        )
        self.pause_btn.bind(on_press=self.pause_bot)
        btn_layout.add_widget(self.pause_btn)
        
        self.stop_btn = Button(
            text="STOP", 
            background_color=(1, 0, 0, 1),
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_bot)
        btn_layout.add_widget(self.stop_btn)
        control_panel.add_widget(btn_layout)
        
        # Stats
        stats_frame = BoxLayout(orientation='vertical', size_hint_y=0.15)
        stats_frame.add_widget(Label(text="STATISTICS", bold=True))
        
        # Counts
        count_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        count_layout.add_widget(Label(text="Completed:"))
        self.completed_label = Label(text="0", bold=True)
        count_layout.add_widget(self.completed_label)
        
        count_layout.add_widget(Label(text="Success:"))
        self.success_label = Label(text="0", color=(0, 1, 0, 1), bold=True)
        count_layout.add_widget(self.success_label)
        
        count_layout.add_widget(Label(text="Failed:"))
        self.failed_label = Label(text="0", color=(1, 0, 0, 1), bold=True)
        count_layout.add_widget(self.failed_label)
        stats_frame.add_widget(count_layout)
        
        # Progress
        self.progress = ProgressBar(max=100, size_hint_y=0.2)
        stats_frame.add_widget(self.progress)
        control_panel.add_widget(stats_frame)
        
        main_layout.add_widget(control_panel)
        
        # Right panel - Progress
        progress_panel = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=10)
        progress_panel.add_widget(Label(text="LIVE PROGRESS", bold=True))
        
        # TreeView in ScrollView
        scroll_view = ScrollView()
        self.tree_view = TreeView(
            size_hint_y=None,
            hide_root=True
        )
        self.tree_view.bind(minimum_height=self.tree_view.setter('height'))
        
        # Create columns
        self.tree_view.add_node(TreeViewLabel(text="ID", width=50, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Status", width=100, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Proxy", width=150, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Message", width=250, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Time", width=100, is_open=True))
        
        scroll_view.add_widget(self.tree_view)
        progress_panel.add_widget(scroll_view)
        
        # Log
        progress_panel.add_widget(Label(text="ACTIVITY LOG", bold=True))
        self.log_area = ScrollView()
        self.log_text = Label(
            text="Application started\n",
            size_hint_y=None,
            text_size=(Window.width - 20, None),
            halign='left',
            valign='top'
        )
        self.log_text.bind(texture_size=self.log_text.setter('size'))
        self.log_area.add_widget(self.log_text)
        progress_panel.add_widget(self.log_area)
        
        main_layout.add_widget(progress_panel)
        self.add_widget(main_layout)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        self.log_text.text += log_line + "\n"
        Logger.info(log_line)

    def set_authentication(self, instance):
        # Try session ID first
        session_id = self.session_id_input.text.strip()
        if session_id:
            self.set_session_id(session_id)
            return
        
        # Try cookie file
        if self.cookie_chooser.selection:
            cookie_file = self.cookie_chooser.selection[0]
            self.import_cookies_from_file(cookie_file)
            return
        
        self.log("Please provide session ID or select cookie file")

    def set_session_id(self, session_id):
        try:
            session_cookie = {
                'name': 'sessionid',
                'value': session_id,
                'domain': '.tiktok.com',
                'path': '/',
                'secure': True,
                'httpOnly': True
            }
            
            self.session_cookies = [session_cookie]
            self.session.cookies.set(session_cookie['name'], session_cookie['value'])
            
            self.auth_status.text = "Authenticated (session ID)"
            self.auth_status.color = (0, 1, 0, 1)
            self.log("Session ID set successfully")
        except Exception as e:
            self.log(f"Error setting session: {str(e)}")
            self.auth_status.text = "Session error"
            self.auth_status.color = (1, 0, 0, 1)

    def import_cookies_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                cookies = json.load(f)
                
            # Validate cookies format
            if not isinstance(cookies, list):
                raise ValueError("Invalid cookies format")
                
            # Apply cookies to session
            for cookie in cookies:
                if 'name' in cookie and 'value' in cookie:
                    self.session.cookies.set(cookie['name'], cookie['value'])
                else:
                    self.log(f"Skipping invalid cookie: {cookie}")
                    
            self.session_cookies = cookies
            self.auth_status.text = f"Authenticated ({len(cookies)} cookies)"
            self.auth_status.color = (0, 1, 0, 1)
            self.log(f"Imported {len(cookies)} cookies from file")
        except Exception as e:
            self.log(f"Error importing cookies: {str(e)}")
            self.auth_status.text = "Import failed"
            self.auth_status.color = (1, 0, 0, 1)

    def load_proxies(self, instance):
        if not self.cookie_chooser.selection:
            self.log("Please select a proxy file")
            return
            
        file_path = self.cookie_chooser.selection[0]
        self.proxy_type = self.proxy_type_spinner.text
        
        try:
            with open(file_path, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            
            # Validate proxy format
            valid_proxies = []
            for proxy in proxies:
                if ':' in proxy and len(proxy.split(':')) >= 2:
                    valid_proxies.append(proxy)
            
            self.proxies = valid_proxies
            self.proxy_status.text = f"{len(self.proxies)} {self.proxy_type} proxies loaded"
            self.log(f"Loaded {len(self.proxies)} proxies")
        except Exception as e:
            self.log(f"Error loading proxies: {str(e)}")

    def start_bot(self, instance):
        # Check authentication
        if not self.session_cookies:
            self.log("Authentication required")
            return
            
        target_url = self.target_input.text.strip()
        if not target_url:
            self.log("Target URL required")
            return
            
        if not self.proxies:
            self.log("Proxies required")
            return
            
        try:
            num_threads = int(self.threads_input.text)
            num_reports = int(self.reports_input.text)
        except ValueError:
            self.log("Invalid thread or report count")
            return
            
        # Parse target URL
        self.target_info = self.parse_target_url(target_url)
        if not self.target_info:
            self.log("Invalid TikTok URL")
            return
            
        # Reset counters
        self.total_reports = num_reports
        self.report_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.progress.value = 0
        
        # Clear tree view
        self.tree_view.clear_widgets()
        self.tree_view.add_node(TreeViewLabel(text="ID", width=50, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Status", width=100, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Proxy", width=150, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Message", width=250, is_open=True))
        self.tree_view.add_node(TreeViewLabel(text="Time", width=100, is_open=True))
        
        # Fill queue
        for _ in range(num_reports):
            self.report_queue.put(self.target_info)
        
        # Start threads
        self.running = True
        self.paused = False
        
        for i in range(num_threads):
            thread = threading.Thread(target=self.worker, args=(i+1,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        # Update UI state
        self.start_btn.disabled = True
        self.pause_btn.disabled = False
        self.stop_btn.disabled = False
        
        self.log(f"Started {num_threads} threads for {num_reports} reports")

    def parse_target_url(self, url):
        """Parse TikTok URL to extract user and video information"""
        result = {"url": url, "type": "video", "id": ""}
        
        try:
            # Extract video ID
            video_match = re.search(r'/video/(\d+)', url)
            if video_match:
                result["id"] = video_match.group(1)
                result["type"] = "video"
                return result
            
            # Extract username
            user_match = re.search(r'@([\w\.]+)', url)
            if user_match:
                result["id"] = user_match.group(1)
                result["type"] = "account"
                return result
            
            # Extract comment ID
            comment_match = re.search(r'/comment/(\d+)', url)
            if comment_match:
                result["id"] = comment_match.group(1)
                result["type"] = "comment"
                return result
            
            return None
        except Exception as e:
            self.log(f"URL parse error: {str(e)}")
            return None

    def pause_bot(self, instance):
        self.paused = not self.paused
        if self.paused:
            self.pause_btn.text = "RESUME"
            self.pause_btn.background_color = (0, 0.7, 0, 1)
            self.log("Reporting paused")
        else:
            self.pause_btn.text = "PAUSE"
            self.pause_btn.background_color = (1, 0.8, 0, 1)
            self.log("Reporting resumed")

    def stop_bot(self, instance):
        self.running = False
        self.paused = False
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1)
        
        self.threads = []
        
        # Reset UI
        self.start_btn.disabled = False
        self.pause_btn.disabled = True
        self.stop_btn.disabled = True
        self.pause_btn.text = "PAUSE"
        self.pause_btn.background_color = (1, 0.8, 0, 1)
        
        self.log(f"Stopped reporting. Completed: {self.report_count}/{self.total_reports}")

    def worker(self, thread_id):
        while self.running and not self.report_queue.empty():
            if self.paused:
                time.sleep(0.5)
                continue
                
            try:
                target_info = self.report_queue.get_nowait()
            except queue.Empty:
                break
                
            proxy = random.choice(self.proxies)
            proxy_parts = proxy.split(':')
            proxy_host = proxy_parts[0]
            proxy_port = proxy_parts[1] if len(proxy_parts) > 1 else '80'
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
                'Referer': 'https://www.tiktok.com/',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://www.tiktok.com',
                'X-Secsdk-Csrf-Token': '000100000001'  # Bypass CSRF protection
            }
            
            try:
                # Get report reason
                reason_text = self.reason_spinner.text
                reason_code = self.report_reasons.get(reason_text, 10015)
                
                # Set up proxy
                proxies = {
                    'http': f'http://{proxy_host}:{proxy_port}',
                    'https': f'http://{proxy_host}:{proxy_port}'
                }
                
                # Prepare payload
                if target_info["type"] == "video":
                    report_url = "https://www.tiktok.com/api/report/item/"
                    payload = {
                        "report_type": reason_code,
                        "item_id": target_info["id"],
                        "owner_id": "",
                        "reason": reason_text,
                        "description": ""
                    }
                elif target_info["type"] == "account":
                    report_url = "https://www.tiktok.com/api/report/user/"
                    payload = {
                        "report_type": reason_code,
                        "object_id": target_info["id"],
                        "owner_id": "",
                        "reason": reason_text,
                        "description": ""
                    }
                else:  # comment
                    report_url = "https://www.tiktok.com/api/report/comment/"
                    payload = {
                        "report_type": reason_code,
                        "comment_id": target_info["id"],
                        "reason": reason_text,
                        "description": ""
                    }
                
                # Send report
                response = self.session.post(
                    report_url,
                    json=payload,
                    headers=headers,
                    proxies=proxies,
                    timeout=15
                )
                
                # Process response
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if response_data.get("status_code") == 0:
                            self.success_count += 1
                            status = "Success"
                            message = f"Reported {target_info['type']}"
                        else:
                            self.failed_count += 1
                            status = "Failed"
                            message = f"API error: {response_data.get('message', 'Unknown')}"
                    except:
                        self.failed_count += 1
                        status = "Failed"
                        message = "Invalid response"
                elif response.status_code == 429:
                    self.failed_count += 1
                    status = "Rate Limited"
                    message = "Too many requests"
                    time.sleep(5)  # Add delay for rate limiting
                else:
                    self.failed_count += 1
                    status = "Failed"
                    message = f"HTTP {response.status_code}"
                
                self.report_count += 1
                
                # Add to progress
                timestamp = datetime.now().strftime("%H:%M:%S")
                progress_entry = {
                    "id": thread_id,
                    "status": status,
                    "proxy": proxy,
                    "message": message,
                    "timestamp": timestamp
                }
                
                # Add to queue for GUI update
                self.report_queue.task_done()
                self.process_gui_updates(progress_entry)
                
                # Random delay
                time.sleep(random.uniform(1.0, 3.0))
                
            except Exception as e:
                self.failed_count += 1
                self.report_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                progress_entry = {
                    "id": thread_id,
                    "status": "Error",
                    "proxy": proxy,
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp
                }
                self.process_gui_updates(progress_entry)
                time.sleep(1)

    def process_gui_updates(self, entry=None, *args):
        if entry:
            # Add to tree view
            self.tree_view.add_node(TreeViewLabel(text=str(entry["id"]), width=50))
            self.tree_view.add_node(TreeViewLabel(text=entry["status"]), width=100))
            self.tree_view.add_node(TreeViewLabel(text=entry["proxy"][:20]), width=150))
            self.tree_view.add_node(TreeViewLabel(text=entry["message"]), width=250))
            self.tree_view.add_node(TreeViewLabel(text=entry["timestamp"]), width=100))
        
        # Update stats
        self.completed_label.text = str(self.report_count)
        self.success_label.text = str(self.success_count)
        self.failed_label.text = str(self.failed_count)
        
        if self.total_reports > 0:
            progress = (self.report_count / self.total_reports) * 100
            self.progress.value = progress

class TikTokReportApp(App):
    def build(self):
        Window.size = (1000, 700)
        return TikTokReportBot()

if __name__ == '__main__':
    TikTokReportApp().run()