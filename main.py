
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass, cast
from android.permissions import request_permissions, Permission
from android import activity
from kivy.clock import mainthread

class MainApp(App):
    def build(self):
        request_permissions([Permission.RECORD_AUDIO])
        self.box = BoxLayout(orientation='vertical')
        self.label = Label(text='برای شروع صحبت روی دکمه کلیک کن')
        self.button = Button(text='شروع ضبط صدا')
        self.button.bind(on_press=self.start_speech)

        self.box.add_widget(self.label)
        self.box.add_widget(self.button)

        activity.bind(on_activity_result=self.on_activity_result)

        return self.box

    def start_speech(self, instance):
        Intent = autoclass('android.content.Intent')
        RecognizerIntent = autoclass('android.speech.RecognizerIntent')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')

        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                        RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "fa-IR")

        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivityForResult(intent, 1001)

    @mainthread
    def on_activity_result(self, requestCode, resultCode, intent):
        if requestCode == 1001 and intent:
            results = intent.getStringArrayListExtra("android.speech.extra.RESULTS")
            if results.size() > 0:
                self.label.text = results.get(0)

if __name__ == '__main__':
    MainApp().run()
