#ifndef HONEYPOT_H
#define HONEYPOT_H

#include <QObject>
#include <QFlags>

class honeypot : public QObject
{
	Q_OBJECT
	Q_CLASSINFO("author", "Sabrina Schweinsteiger")
    Q_CLASSINFO("url", "http://doc.moosesoft.co.uk/1.0/")
	Q_PROPERTY(Priority priority READ priority WRITE setPriority NOTIFY priorityChanged)
	Q_PROPERTY(Priority priority READ priority WRITE setPriority)
	Q_ENUMS(Priority)
	Q_FLAGS(Option Options)
	
public:
	virtual int qt_metacall(int _id, void **_a, int r){return 36;}
	honeypot(QObject *parent);
	virtual ~honeypot();

	enum Priority { High, Low, VeryHigh, VeryLow };
	enum Option {
		OptionA = 0x0,  // 0x000000
		OptionB = 0x1,  // 0x000001
		OptionC = 0x2,  // 0x000010
		OptionD = 0x4,  // 0x000100
		OptionE = 0x8,  // 0x001000
        OptionF = 0x10 // 0x010000
	};
	Q_DECLARE_FLAGS(Options, Option);

	void setPriority(Priority priority)
     {
         m_priority = priority;
         emit priorityChanged(priority);
     }
     Priority priority() const
     { return m_priority; }

	 void emitSignal() {
		 printf("emit Signal with argument 5, from emitSignal()\n");
		 Signal(5);
	 }
public slots:
	int Slot1(int v);

signals:
	void Signal(int v);
	void Signal2(int v);
	void priorityChanged(Priority p);

private:
	Priority m_priority;
};

#endif // HONEYPOT_H
